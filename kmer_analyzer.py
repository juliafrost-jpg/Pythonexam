# Import the sys module so we can access command-line arguments
import sys


# Function to validate whether a sequence is usable
def validate_sequence(sequence, k):

    # Check if the sequence length is shorter than k
    # If it is, the sequence cannot contain any k-mers
    if len(sequence) < k:
        return False

    # Create a set of allowed DNA characters
    valid_chars = {'A', 'C', 'G', 'T'}

    # Loop through every nucleotide in the sequence
    for nucleotide in sequence:

        # Convert the nucleotide to uppercase and check if it is valid
        if nucleotide.upper() not in valid_chars:

            # Return False if an invalid character is found
            return False

    # Return True if the sequence passes all checks
    return True


# Function to update counts for a k-mer and its following character
def update_kmer_count(kmer_data, kmer, next_char):

    # Check if this k-mer has not been seen before
    if kmer not in kmer_data:

        # Create a new dictionary entry for this k-mer
        kmer_data[kmer] = {

            # Store the total number of times the k-mer appears
            'count': 0,

            # Store counts of characters that follow this k-mer
            'next_chars': {}
        }

    # Increase the total count for this k-mer
    kmer_data[kmer]['count'] += 1

    # Check if this next character has not been seen before
    if next_char not in kmer_data[kmer]['next_chars']:

        # Initialize the next character count to zero
        kmer_data[kmer]['next_chars'][next_char] = 0

    # Increase the count for this next character
    kmer_data[kmer]['next_chars'][next_char] += 1

    # Return the updated dictionary
    return kmer_data


# Function to count all k-mers and their following characters
def count_kmers_with_context(sequence, k):

    # Create an empty dictionary to store k-mer information
    kmer_data = {}

    # Loop through the sequence
    # Stop at len(sequence) - k so we do not go out of range
    for i in range(len(sequence) - k):

        # Extract a substring of length k starting at position i
        kmer = sequence[i:i+k]

        # Get the character immediately after the k-mer
        next_char = sequence[i+k]

        # Update counts for this k-mer and following character
        update_kmer_count(kmer_data, kmer, next_char)

    # Return the completed dictionary of k-mer data
    return kmer_data


# Function to write the k-mer results to an output file
def write_results_to_file(kmer_data, output_filename):

    # Sort all k-mers alphabetically
    sorted_kmers = sorted(kmer_data.keys())

    # Open the output file in write mode
    with open(output_filename, 'w') as f:

        # Loop through every sorted k-mer
        for kmer in sorted_kmers:

            # Get the total count for this k-mer
            count = kmer_data[kmer]['count']

            # Get the dictionary of next-character frequencies
            next_chars = kmer_data[kmer]['next_chars']

            # Create a formatted string of next-character counts
            # Example: A:2 C:1 G:4
            next_char_str = " ".join(

                # Format each character-frequency pair
                f"{char}:{freq}"

                # Sort the next characters alphabetically
                for char, freq in sorted(next_chars.items())
            )

            # Write the formatted results to the file
            f.write(f"{kmer} count:{count} {next_char_str}\n")


# Main function that controls the program
def main():

    # Get the input sequence filename from the command line
    sequence_file = sys.argv[1]

    # Get the k-mer size from the command line and convert to integer
    k = int(sys.argv[2])

    # Get the output filename from the command line
    output_file = sys.argv[3]

    # Print a message showing which file is being read
    print(f"Reading sequences from {sequence_file}...")

    # Create a dictionary to store combined results from all sequences
    combined_kmer_data = {}

    # Open the sequence file for reading
    with open(sequence_file, 'r') as f:

        # Loop through every line in the file
        for sequence in f:

            # Remove spaces and newline characters from the sequence
            sequence = sequence.strip()

            # Validate the sequence before processing
            if not validate_sequence(sequence, k):

                # Print a warning if the sequence is invalid
                print("Warning: Skipping invalid sequence")

                # Skip to the next sequence
                continue

            # Count k-mers for the current sequence
            sequence_kmers = count_kmers_with_context(sequence, k)

            # Loop through every k-mer in this sequence
            for kmer in sequence_kmers:

                # Check if the k-mer is not already in the combined dictionary
                if kmer not in combined_kmer_data:

                    # Create a new entry for this k-mer
                    combined_kmer_data[kmer] = {

                        # Initialize the total count
                        'count': 0,

                        # Initialize the next-character dictionary
                        'next_chars': {}
                    }

                # Add this sequence's count to the combined count
                combined_kmer_data[kmer]['count'] += sequence_kmers[kmer]['count']

                # Loop through all next-character counts for this k-mer
                for char, freq in sequence_kmers[kmer]['next_chars'].items():

                    # Check if this next character is new
                    if char not in combined_kmer_data[kmer]['next_chars']:

                        # Initialize the next-character count
                        combined_kmer_data[kmer]['next_chars'][char] = 0

                    # Add the frequency to the combined total
                    combined_kmer_data[kmer]['next_chars'][char] += freq

    # Write all combined results to the output file
    write_results_to_file(combined_kmer_data, output_file)


# Check whether this script is being run directly
if __name__ == '__main__':

    # Run the main function
    main()
