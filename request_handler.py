from reactions.request import add_reaction, create_reaction
from comments.request import delete_comment, update_comment
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts import ( get_posts_by_user_id, 
                    get_post_by_id, 
                    create_post,
                    get_all_posts,
                    delete_post,
                    update_post,
                    approve_post )
from comments import create_comment, get_all_comments
from users import register_new_user, existing_user_check, get_all_users
from categories import get_all_categories, create_category, delete_category, update_category
from tags import create_tag, get_all_tags, delete_tag, update_tag

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com
            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'
            return ( resource, key, value )
        # No query string parameter
        else:
            id = None
            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/
            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            if resource == "categories":
                if id is not None:
                    pass
                else:
                    response = get_all_categories()
            elif resource == "tags":
                if id is not None:
                    pass
                else:
                    response = get_all_tags()
            elif resource == "posts":
                if id is not None:
                    response = get_post_by_id(id)
                else:
                    response = get_all_posts()
            elif resource == "comments":
                if id is not None:
                    pass
                else:
                    response = get_all_comments()
        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            if key == "userId" and resource == "posts":
                response = get_posts_by_user_id(value)
        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_creation = None

        if resource == "postreactions":
            new_creation = add_reaction(post_body)
        elif resource == "reactions":
            new_creation = create_reaction(post_body)
        elif resource == "posts":
            new_creation = create_post(post_body)
        elif resource == "comments":
            new_creation = create_comment(post_body)
        elif resource == "users":
            new_creation = register_new_user(post_body)
        elif resource == "login":
            new_creation = existing_user_check(post_body)
        elif resource == "tags":
            new_creation = create_tag(post_body)
        elif resource == "categories":
            new_creation = create_category(post_body)

        self.wfile.write(new_creation.encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        success = False
        if resource == "tags":
            success = update_tag(id, post_body)
        elif resource == "comments":
            success = update_comment(id, post_body)
        elif resource == "categories":
            success = update_category(id, post_body)
        elif resource == "posts":
            success = update_post(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_PATCH(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False
        if resource == "approve":
            success = approve_post(id)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)
        elif resource == "comments":
            delete_comment(id)
        elif resource == "tags":
            delete_tag(id)
        elif resource == "categories":
            delete_category(id)

        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
