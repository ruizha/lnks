from flask import Flask, request, jsonify, abort

router = Flask(__name__)

# In-memory dictionary to store shortname-URL mappings
# In a real application, this would be a database or persistent storage
url_mappings : dict[str, str] = {}

@router.route('/goto/<shortname>', methods=['GET'])
def goto_url(shortname: str):
    print(f"Got shortname: {shortname}")
    if not shortname:
        abort(400, description="Missing 'shortname' parameter")

    print(url_mappings)
    full_url = url_mappings.get(shortname)
    if full_url:
        return jsonify({"full_url": full_url})
    else:
        abort(404, description=f"Shortname '{shortname}' not found")

@router.route('/link', methods=['POST'])
def link_url():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON data")

    print(data.get('shortname'))
    print(data.get('full_url'))

    shortname = data.get('shortname')
    full_url = data.get('full_url')

    if not shortname or not full_url:
        abort(400, description="Missing 'shortname' or 'full_url' in request body")

    url_mappings[shortname] = full_url
    return jsonify({"message": f"Shortname '{shortname}' linked to '{full_url}' successfully"}), 201