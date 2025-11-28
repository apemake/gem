                                                                               
import os                                                                     
import sys                                                                    
import glob                                                                   
                                                                              
def estimate_chunks(chat_dir):                                                
    """                                                                       
    Counts the number of chat log chunks in a directory.                      
    """                                                                       
    search_pattern = os.path.join(chat_dir, '*_clean.txt')                    
                                                                              
    try:                                                                      
        # Find all chunk files                                                
        chunk_files = glob.glob(search_pattern)                               
                                                                              
        num_chunks = len(chunk_files)                                         
                                                                              
        print(f"Found {num_chunks} chat chunk(s) in the specified directory.")
        print(f"This corresponds to {num_chunks} 'notebook(s)' for a full summ
arization run.")                                                              
                                                                              
    except Exception as e:                                                    
        print(f"An error occurred: {e}")                                      
                                                                              
if __name__ == "__main__":                                                    
    if len(sys.argv) != 2:                                                    
        print("Usage: python estimate_chunks.py <path_to_cleaned_chat_chunks_d
irectory>")                                                                   
        sys.exit(1)                                                           
                                                                              
    chat_chunk_dir = sys.argv[1]                                              
    estimate_chunks(chat_chunk_dir)