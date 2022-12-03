# distributed microblog

The 5_microblog_broadcast.py file defines a peer-to-peer (P2P) network for microblogging. The network consists of MicroblogPost objects that represent individual posts, MicroblogNode objects that represent individual nodes in the network, and a MicroblogNetwork object that represents the network as a whole.

Each MicroblogNode has a username, an IP address, and a port number. The node listens for incoming connections on its port and accepts incoming connections from other nodes in the network. When a new connection is accepted, the node receives a microblog post from the connected node and adds it to its list of posts.

The MicroblogNode class also provides methods for adding and connecting to peer nodes, broadcasting a microblog post to all connected peer nodes, and broadcasting the node's IP address to all connected peer nodes.

The MicroblogNetwork class provides a broadcast_post method for broadcasting a microblog post to all nodes in the network.

The main function creates a new MicroblogNetwork object, creates two MicroblogNode objects and adds them to the network, connects the nodes to each other, broadcasts a microblog post, and prints the list of posts received by the second node.
