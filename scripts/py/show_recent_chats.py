                                                                               
import os                                                                     
import sys                                                                    
import glob                                                                   
                                                                              
def show_recent_chats(chat_dir, num_files):                                   
    """
    Shows the content of the most recent chat log chunks.                     
    """
    # The script looks for files ending with _clean.txt in the specified direc
tory.                                                                         
    search_pattern = os.path.join(chat_dir, '*_clean.txt')                    
                                                                              
    try:                                                                      
        # Find all chunk files                                                
        chunk_files = glob.glob(search_pattern)                               
                                                                              
        if not chunk_files:                                                   
            print(f"No chat chunks found in: {chat_dir}")                     
            return                                                            
                                                                              
        # Sort files by modification time, newest first                       
        chunk_files.sort(key=os.path.getmtime, reverse=True)                  
                                                                              
        # Get the requested number of recent files                            
        files_to_show = chunk_files[:num_files]                               
                                                                              
        print(f"--- Showing content of the {len(files_to_show)} most recent ch
at(s) ---")                                                                   
                                                                              
        # Reverse the list to show the oldest of the selection first, for chro
nological order                                                               
        for file_path in reversed(files_to_show):                             
            print(f"\n--- Content of {os.path.basename(file_path)} ---\\n")    
            with open(file_path, 'r', errors='ignore') as f:                  
                print(f.read())                                               
                                                                              
    except Exception as e:                                                    
        print(f"An error occurred: {e}")                                      
                                                                              
if __name__ == "__main__":                                                    
    if len(sys.argv) < 2:                                                     
        print("Usage: python show_recent_chats.py <path_to_cleaned_chat_chunks
_directory> [num_files]")                                                     
        sys.exit(1)                                                           
                                                                              
    chat_chunk_dir = sys.argv[1]                                              
                                                                              
    num_to_show = 1                                                           
    if len(sys.argv) > 2:                                                     
        try:                                                                  
            num_to_show = int(sys.argv[2])                                    
        except ValueError:                                                    
            print("Error: num_files must be an integer.")                     
            sys.exit(1)                                                       
                                                                              
    show_recent_chats(chat_chunk_dir, num_to_show)
