import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts import ( get_posts_by_user_id, 
                    get_post_by_id, 
                    create_post,
                    get_all_posts,
                    delete_post )
from comments import create_comment, get_all_comments
from users import register_new_user, existing_user_check
from users import register_new_user
from categories import get_all_categories, create_category, delete_category
from tags import create_tag, get_all_tags, delete_tag

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
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

    # Here's a class function
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

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

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
            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
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

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            elif key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)
            elif key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)
            elif key == "userId" and resource == "posts":
                response = get_posts_by_user_id(value)
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        #reads up to the end of the characters
        content_len = int(self.headers.get('content-length', 0))
        #turns that string into a python dictionary
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_creation = None

        if resource == "posts":
            new_creation = create_post(post_body)
        if resource == "comments":
            new_creation = create_comment(post_body)
        if resource == "users":
            new_creation = register_new_user(post_body)
        if resource == "login":
            new_creation = existing_user_check(post_body)
        if resource == "tags":
            new_creation = create_tag(post_body)
        if resource == "categories":
            new_creation = create_category(post_body)

        self.wfile.write(new_creation.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            pass
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)
        elif resource == "tags":
            delete_tag(id)
        elif resource == "categories":
            delete_category(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


# how to run the file if using the debugger
if __name__ == "__main__":
    main()
