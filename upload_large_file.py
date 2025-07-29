import dropbox
import os
from dropbox_auth import authenticate_dropbox

def upload_large_file(dbx, local_path, dropbox_path, chunk_size=4 * 1024 * 1024):
    """Uploads a large file (> 150 MB) to Dropbox using an upload session."""
    try:
        file_size = os.path.getsize(local_path)
        with open(local_path, 'rb') as f:
            # Start session
            upload_session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=f.tell())
            commit = dropbox.files.CommitInfo(path=dropbox_path, mode=dropbox.files.WriteMode('overwrite'))
            
            print(f"Uploading '{local_path}'... {f.tell() / file_size:.0%}")

            # Append remaining chunks
            while f.tell() < file_size:
                if (file_size - f.tell()) <= chunk_size:
                    dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit)
                    break
                else:
                    dbx.files_upload_session_append_v2(f.read(chunk_size), cursor)
                    cursor.offset = f.tell()
                print(f"Uploading '{local_path}'... {f.tell() / file_size:.0%}")
            
            print(f"Successfully uploaded '{local_path}' to '{dropbox_path}'")

    except FileNotFoundError:
        print(f"Error: Local file '{local_path}' not found.")
    except dropbox.exceptions.ApiError as e:
        print(f"API error uploading large file: {e}")

if __name__ == '__main__':
    dbx = authenticate_dropbox()
    
    if dbx:
        # Example usage (replace with actual file path)
        # Create a dummy large file for testing: fsutil file createnew large_file.bin 160000000
        upload_large_file(dbx, "large_file.bin", "/large_files/large_file.bin") 