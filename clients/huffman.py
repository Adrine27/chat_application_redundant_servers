import heapq
from collections import defaultdict

def huffman_encoding(message):
    # create frequency dictionary
    freq_dict = defaultdict(int)
    for c in message:
        freq_dict[c] += 1

    # create heap
    heap = [[freq, [char, ""]] for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    # combine nodes until there is only one node left
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])

    # generate Huffman encoding dictionary
    encoding_dict = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))

    # generate Huffman encoded message
    encoded_message = ""
    for c in message:
        encoded_message += encoding_dict[c]

    # pad the message with zeroes so its length is a multiple of 8
    padding_length = (8 - len(encoded_message) % 8) % 8
    encoded_message += "0" * padding_length

    # convert the binary string to bytes
    encoded_bytes = int(encoded_message, 2).to_bytes(len(encoded_message) // 8, byteorder='big')

    return encoded_bytes, encoding_dict

def huffman_decoding(encoded_message, encoding_dict):
    # Create a new dictionary with switched key-value pairs
    decoding_dict = {v: k for k, v in encoding_dict.items()}

    # Convert the bytes to a binary string
    binary_string = ''.join(f"{byte:08b}" for byte in encoded_message)

    # Remove the padding zeroes
    binary_string = binary_string.rstrip('0')

    # Decode the message using the decoding dictionary
    decoded_message = ""
    current_code = ""
    for bit in binary_string:
        current_code += bit
        if current_code in decoding_dict:
            decoded_message += decoding_dict[current_code]
            current_code = ""
    return decoded_message
