##### Backend #######
1. Run shell file 
    sh setup.sh
2. Command to Run Flask :
    python3 analyze.py

3. Command to run analyze the file:
    curl -X POST -v -F "file=@image.png" http://127.0.0.1:5000/analyze