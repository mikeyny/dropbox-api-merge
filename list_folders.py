import dropbox
from dropbox_auth import authenticate_dropbox

def list_folder_contents(dbx, folder_path=""):
    """
    Lists the contents of a Dropbox folder, handling pagination.
    An empty folder_path represents the root directory.
    """
    try:
        result = dbx.files_list_folder(folder_path)
        entries = result.entries
        
        # Paginate if there are more entries
        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            entries.extend(result.entries)
            
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                print(f"- File: {entry.name} (ID: {entry.id})")
            elif isinstance(entry, dropbox.files.FolderMetadata):
                print(f"- Folder: {entry.name} (ID: {entry.id})")
                
    except dropbox.exceptions.ApiError as e:
        print(f"API error listing folder '{folder_path}': {e}")

if __name__ == '__main__':
    dbx = authenticate_dropbox()
    
    if dbx:
        print("\nListing root folder contents:")
        list_folder_contents(dbx, "")  # List root
        
        print("\nListing contents of '/DesignMate' (if exists):")
        list_folder_contents(dbx, "/DesignMate")  # List a specific folder 