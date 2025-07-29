import dropbox
from dropbox_auth import authenticate_dropbox

def download_file(dbx, dropbox_path, local_path):
    """Downloads a file from Dropbox."""
    try:
        metadata, res = dbx.files_download(path=dropbox_path)
        with open(local_path, 'wb') as f:
            f.write(res.content)
        print(f"Successfully downloaded '{dropbox_path}' to '{local_path}'")
        print(f"Metadata: Name: {metadata.name}, Size: {metadata.size} bytes")
    except dropbox.exceptions.HttpError as e:
        print(f"HTTP error downloading file: {e}")
    except dropbox.exceptions.ApiError as e:
        print(f"API error downloading file: {e.path_lookup}")

if __name__ == '__main__':
    dbx = authenticate_dropbox()
    
    if dbx:
        # Example usage (replace with actual file paths)
        download_file(dbx, "/reports/2024_report.pdf", "downloaded_report.pdf") 