import dropbox
from dropbox_auth import authenticate_dropbox

def upload_small_file(dbx, local_path, dropbox_path):
    """Uploads a small file (< 150 MB) to Dropbox."""
    try:
        with open(local_path, 'rb') as f:
            dbx.files_upload(
                f.read(), 
                dropbox_path, 
                mode=dropbox.files.WriteMode('overwrite')
            )
        print(f"Successfully uploaded '{local_path}' to '{dropbox_path}'")
    except FileNotFoundError:
        print(f"Error: Local file '{local_path}' not found.")
    except dropbox.exceptions.ApiError as e:
        print(f"API error uploading file: {e}")

if __name__ == '__main__':
    dbx = authenticate_dropbox()
    
    if dbx:
        # Example usage (replace with actual file paths)
        upload_small_file(dbx, "report.pdf", "/reports/2024_report.pdf") 