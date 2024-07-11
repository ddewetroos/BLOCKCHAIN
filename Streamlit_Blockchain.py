import streamlit as st
import datetime as date
import hashlib
import base64
import pandas as pd


# Define the Block class
class Block:
    def __init__(self, index, timestamp, name, unique_id, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.name = name
        self.unique_id = unique_id
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(str(self.index).encode() +
                              str(self.timestamp).encode() +
                              str(self.name).encode() +
                              str(self.unique_id).encode() +
                              str(self.data).encode() +
                              str(self.previous_hash).encode()).hexdigest()


# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", 0, "Genesis Data", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


# Function to display blockchain
def display_blockchain(blockchain):
    st.subheader("Blockchain")
    for block in blockchain.chain:
        st.write(f"Index: {block.index}")
        st.write(f"Timestamp: {block.timestamp}")
        st.write(f"Name: {block.name}")
        st.write(f"Unique ID: {block.unique_id}")
        st.write(f"Data: {block.data}")
        st.write(f"Previous Hash: {block.previous_hash}")
        st.write(f"Hash: {block.hash}")
        st.write("")


# Function to add block
def add_block(blockchain, name, unique_id, uploaded_file):
    latest_block = blockchain.get_latest_block()
    file_contents = uploaded_file.getvalue()
    new_block = Block(latest_block.index + 1, date.datetime.now(), name, unique_id, uploaded_file.name,
                      latest_block.hash)
    blockchain.add_block(new_block)
    st.success("Block added successfully!")


# Function to generate and download verification document
def generate_verification_doc(blockchain):
    data_list = []
    for block in blockchain.chain:
        data_list.append({
            'Index': block.index,
            'Timestamp': block.timestamp,
            'Name': block.name,
            'Unique ID': block.unique_id,
            'Data': block.data,
            'Previous Hash': block.previous_hash,
            'Hash': block.hash
        })

    df = pd.DataFrame(data_list)

    st.write("Verification Document Generated:")
    st.write(df)

    st.subheader("Download Verification Document")
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="blockchain_verification.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


# Main function
def main():
    st.title("Blockchain with File Upload, Name, and Unique ID")

    # Create a blockchain instance
    blockchain = Blockchain()

    # Display current blockchain
    display_blockchain(blockchain)

    # Upload file for new block
    st.subheader("Add a New Block with File Upload, Name, and Unique ID")
    name = st.text_input("Enter Name:")
    unique_id = st.number_input("Enter Unique ID:", step=1, min_value=0)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        if st.button("Add Block"):
            add_block(blockchain, name, unique_id, uploaded_file)
            display_blockchain(blockchain)
            st.info("To verify the blockchain, download the verification document below.")

    # Generate and download verification document
    st.subheader("Generate Verification Document")
    if st.button("Generate"):
        generate_verification_doc(blockchain)


if __name__ == "__main__":
    main()
