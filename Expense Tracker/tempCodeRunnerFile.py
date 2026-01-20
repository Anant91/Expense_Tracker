ort.xlsx"})

@app.route('/api/export/download', methods=['GET'])
def export_download():
    # for demo, return a small CSV file generated on the fly
    from io import BytesIO
    f = BytesIO()
    f.write(b"id,date,amount,category,note\n1,2025-11-25,100,food,pizza\n")