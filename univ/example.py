import memcache
"""
Example class
 
This is simply an example class used for the memcache demonstration
 
package: echolibre.examples
"""
class Example():
    """Example of memcache tester"""
    hostname = ""
    server   = ""
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server   = memcache.Client([self.hostname])
 
    def set(self, key, value, expiry=900):
        """
        This method is used to set a new value
        in the memcache server.
        """
        self.server.set(key, value, expiry)
 
    def get(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        return self.server.get(key)
 
    def delete(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        self.server.delete(key)
 
if __name__ == '__main__':
    sample = Example("127.0.0.1");
    sample.set("name", "david");
    retrieved = sample.get("name");
    print retrieved