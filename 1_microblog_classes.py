# Import the necessary libraries
import hashlib
import json
from typing import Dict, List
import time

# Define the data structure for a microblog post
class MicroblogPost:
  def __init__(self, username: str, content: str):
    self.username = username
    self.content = content
    self.timestamp = time.time()
  
  # Generate a unique ID for the post
  def generate_id(self) -> str:
    # Hash the post content and the timestamp
    post_data = (self.content + str(self.timestamp)).encode()
    hashed_data = hashlib.sha256(post_data).hexdigest()
    # Return the hashed data as the post ID
    return hashed_data

# Define the P2P network node
class MicroblogNode:
  def __init__(self, node_id: str, username: str):
    self.node_id = node_id
    self.username = username
    self.posts = [] # List of microblog posts
    self.peers = [] # List of peer nodes
  
  # Add a new microblog post to the node
  def add_post(self, post: MicroblogPost):
    self.posts.append(post)
  
  # Get all microblog posts from the node
  def get_posts(self) -> List[MicroblogPost]:
    return self.posts
  
  # Add a new peer node to the network
  def add_peer(self, peer: 'MicroblogNode'):
    self.peers.append(peer)
  
  # Get a list of all peer nodes in the network
  def get_peers(self) -> List['MicroblogNode']:
    return self.peers

# Define the P2P network
class MicroblogNetwork:
  def __init__(self):
    self.nodes = {} # Dictionary of nodes in the network
  
  # Add a new node to the network
  def add_node(self, node: MicroblogNode):
    self.nodes[node.node_id] = node
  
  # Get a list of all nodes in the network
  def get_nodes(self) -> List[MicroblogNode]:
    return self.nodes.values()
  
  # Broadcast a microblog post to all nodes in the network
  def broadcast_post(self, post: MicroblogPost):
    for node in self.nodes.values():
      node.add_post(post)

# Create a new microblog post
post = MicroblogPost('johndoe', 'Hello, world!')

# Create a new node and add it to the network
node = MicroblogNode('node1', 'johndoe')
network = MicroblogNetwork()
network.add_node(node)

# Add a second node to the network
node2 = MicroblogNode('node2', 'janedoe')
network.add_node(node2)

# Connect the nodes to each other
node.add_peer(node2)
node2.add_peer(node)

# Broadcast the microblog post to all nodes in the network
network.broadcast_post(post)

# Get the list of all nodes in the network
nodes = network.get_nodes()

# Print the microblog posts from all nodes in the network
for node in nodes:
  print(f'Username: {node.username}')
  print(f'Node ID: {node.node_id}')
  print('Posts:')
  for post in node.get_posts():
    print(f'  - {post.content}')
  print()

