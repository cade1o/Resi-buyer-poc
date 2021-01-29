import json
import pickle
import time
import requests

from .models import Order, Information
from .utils.Blockchain import Blockchain, Block
from .utils.tracking_info import add_first_tracking_item, add_next_tracking_item, generate_full_tracking
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


'''
Note(ragavsachdeva):
For now, I have put in a placeholder http response as the default.
Moving forward we should really be using class-based views (see: https://docs.djangoproject.com/en/3.1/topics/class-based-views/)
and templates (see: https://docs.djangoproject.com/en/3.1/topics/templates/#:~:text=A%20Django%20template%20is%20a,is%20rendered%20with%20a%20context.)
'''
def index(request):
    if request.user.is_authenticated:
        return render(request, 'UI/index/index.html')
    return redirect('login')

def order_place(request):
    if request.user.is_authenticated:
        return render(request, 'UI/order_place/order_place.html')
    return redirect('login')

def order_view(request):
    if not request.user.is_authenticated:
            return redirect('login')
    try:
        orders = Order.objects.filter(user=request.user.username)
    except Order.DoesNotExist:
        orders = []
    return render(request,'UI/order_view/order_view.html',{'orders': orders})

def checkout(request):
    if request.user.is_authenticated:
        return HttpResponse('Hello, this is the checkout page')
    return redirect('login')

def register(request):
    if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request,'Your account has been created!')
             return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'UI/authentication_page/register.html',{'form': form})

def place_order(request):
    if request.method == 'POST':
        order_data = request.POST
        new_order = Order(user=request.user.username,\
                        product_name=order_data['product_name'],\
                        producer_name=order_data['producer_name'],\
                        quantity=order_data['quantity'],\
                        delivery_address=f"{order_data['delivery_address']}, {order_data['country']}, {order_data['state']}, {order_data['zip']}")
        new_order.save()
        add_first_tracking_item(new_order)
        return HttpResponseRedirect('../order/place/')
    else:
        return HttpResponse(status=404)

def make_invoice(request, order_id):

    # Handle if the user isn't logged in
    if not request.user.is_authenticated:
        return redirect('logon')
    
    # Attempt to get the order with the correct order_id
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'UI/index/index.html')
    
    # Check if the user is the one who made the order
    if order.user != request.user.username:
        return render(request, 'UI/index/index.html')
    
    # Get the tracking info
    tracking_info = Information.objects.filter(order_id=order_id)
    
    return render(request,'UI/invoice/invoice.html', {'name': order.user, 'order': order, 'tracking_info': tracking_info})

# Add a single new piece of tracking info to the order with order_id
def add_tracking_info(request, order_id):
    add_next_tracking_item(order_id)
    return HttpResponseRedirect('../../invoice/' + str(order_id) + '/')

# Add the rest of the tracking info to the order with order_id
def generate_full_tracking_info(request, order_id):
    generate_full_tracking(order_id)
    return HttpResponseRedirect('../../invoice/' + str(order_id) + '/')

# Add a piece of tracking info to the database
def add_database(**kwargs):
    tracking_data = Information(**kwargs)
    tracking_data.save()

# --- Blockchain ---

blockchain_file_name = "saved_blockchain"
peers_file_name = "saved_peers"

# Save the current blockchain so that it can persist between sessions
def save_peers_to_file():
    with open(peers_file_name, 'wb') as f:
        pickle.dump(peers, f)

# Load the blockchain from the file (raising an error if it failed)
def load_peers_from_file():
    with open(peers_file_name, 'rb') as f:
        return pickle.load(f)
    raise Exception("Peers were not successfully loaded from file")

# Save the current blockchain so that it can persist between sessions
def save_blockchain_to_file():
    with open(blockchain_file_name, 'wb') as f:
        pickle.dump(blockchain, f)

# Load the blockchain from the file (raising an error if it failed)
def load_blockchain_from_file():
    with open(blockchain_file_name, 'rb') as f:
        return pickle.load(f)
    raise Exception("Blockchain wasn't successfully loaded from file")

# Crate a new blockchain and mine the first block
def create_new_blockchain():
    new_blockchain = Blockchain()
    new_blockchain.create_genesis_block()
    return new_blockchain

# Loading the Blockchain and Peers From files
blockchain = load_blockchain_from_file()
peers = load_peers_from_file()

# Show the page with all the blockchain blocks listed
def view_blockchain(request):
    return render(request,'UI/blockchain/blockchain.html', {'blocks': blockchain.chain, 'txs': blockchain.unconfirmed_data})

# Retrieves the blockchain from the end point
def get_blockchain(request):
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    data = json.dumps({"length": len(chain_data),
                       "chain": chain_data})
    return HttpResponse(content=data, content_type="application/json")

# Creates a chain from response json
def create_chain_from_dump(chain_dump):
    new_blockchain = Blockchain()
    for idx, block_data in enumerate(chain_dump):
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"])
        proof = block_data['hash']
        if idx > 0:
            added = new_blockchain.add_block(block, proof)
            if not added:
                raise Exception("The chain dump is tampered!!")
        else:  # the block is a genesis block, no verification needed
            new_blockchain.chain.append(block)
    return new_blockchain

# Check if there is concensus between the peers on the longest chain
def consensus(current_host):

    longest_chain = None
    current_len = len(blockchain.chain)
    print("Current Length: {}".format(current_len))
    for node in peers:
        if (node != current_host):
            text = 'http://{}/get_chain/'.format(node)
            try:
                response = requests.get(text)
                length = response.json()['length']
                print("Node: {}".format(node))
                print("Response Chain Length: {}".format(length))
                chain = response.json()['chain']

                if length > current_len and blockchain.check_chain_validity(chain):
                    # Longer valid chain found!
                    current_len = length
                    longest_chain = chain
            except:
                print("Error Occurred")

    if longest_chain:
        blockchain.set_chain(longest_chain) 
        return True

    return False


# Register a new node in the Blockchain peer to peer network
def register_node(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_data = request.POST
            node_address = post_data['node_address']
            if not node_address:
                return render(request, 'UI/register_node/register_node.html',{'peers': peers, 'error':True})
            # Add the node to the peer list
            peers.add(node_address)

            # Return to peers page
            return render(request, 'UI/register_node/register_node.html',{'peers': peers, 'success':True})
        else:
            return render(request, 'UI/register_node/register_node.html', {'peers': peers})
    return redirect('login')

# Add the data to the unconfirmed data of the blockchain
def add_to_unconfirmed(data):
    blockchain.add_new_data(data)

# Broadcasts new transactions to all peers. Tx = Transactions
def broadcast_tx(new_tx):
    for peer in peers:
        res = dict.fromkeys({0},new_tx)
        url = "http://{}/add_tx/".format(peer)
        try:
            requests.post(url, data=res)
        except:
            print("Could not connect to {}".format(url))
# Receives any transactions that have been broadcast. Tx = Transactions
# Is CSRF exempt as blockchain checks will catch bad input
@csrf_exempt
def receive_unconfirmed_tx(request):
    if request.method == "POST":
        new_tx = request.POST.get('0')
        if new_tx != blockchain.last_tx:
            add_to_unconfirmed(new_tx)
            return HttpResponse("Transaction Added", content_type="text/plain",status=200)
        else: 
            return HttpResponse("Transaction Already Added", content_type="text/plain",status=200)

# Function to announce the new blocks to other peers
def announce_new_block(block, current_host):
    for peer in peers:
        if (peer != current_host):
            url = "http://{}/add_block/".format(peer)
            new_block = block.__dict__
            try:
                requests.post(url, data=new_block)
            except:
                print("Could not connect to {}".format(url))


# Receives the new block from the end point and adds it to the chain
# Is CSRF exempt as blockchain checks will catch bad input
@csrf_exempt
def verify_and_add_block(request):
    if request.method == 'POST':
        block_data = request.POST
    
        block = Block(int(block_data.get("index")),
                    block_data.getlist("data"),
                    float(block_data.get("timestamp")),
                    block_data.get("previous_hash"))
        block.nonce = int(block_data.get("nonce"))
        proof = block_data.get('hash')
        added = blockchain.add_block(block, proof)

        if not added:
            return HttpResponse("Block Discarded by node", content_type="text/plain",status=400)
        return HttpResponse("Block Added to the chain", content_type="text/plain",status=200)
    return HttpResponse("No Block Received", content_type="text/plain",status=400)

# Reset blockchain locations in the database
def reset_blockchain_location(new_block_loc):
    data = Information.objects.filter(block_loc=-1)
    for item in data:
        if item.previous_hash == NULL:
            item.update(block_loc=new_block_loc)
        else :
            item.update(previous_block_loc=new_block_loc, block_loc=new_block_loc) 
# Add all the blockchain's unconfirmed data into the next block
# Redirects the user to the to index page
def mine_unconfirmed_data(request):
    result = blockchain.mine()
    if not result:
        return HttpResponse("No Transactions to mine", content_type="text/plain",status=400)
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        current_host =  request.get_host()
        consensus(current_host)
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block(blockchain.last_block, current_host)
            save_blockchain_to_file()
            reset_blockchain_location(blockchain.last_block.index)
            text = "Block #{} is mined.".format(blockchain.last_block.index)
        return HttpResponse(text, content_type="text/plain", status=200)