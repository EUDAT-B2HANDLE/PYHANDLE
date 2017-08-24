class HandleClient(object):
    HANDLE_CLIENT = None

    def retrieve_handle_record_json(self, handle):
        raise NotImplementedError()

    def retrieve_handle_record(self, handle):
        raise NotImplementedError()

    def modify_handle_value(self, handle, ttl=None, add_if_not_exist=True, **kvpairs):
        raise NotImplementedError()

    def list_all_handles(self):
        raise NotImplementedError()

    def generate_and_register_handle(self, prefix, location, checksum=None, **extratypes):
        raise NotImplementedError()

    def delete_handle_value(self, handle, key):
        raise NotImplementedError()

    def delete_handle(self, handle):
        raise NotImplementedError()

    def instantiate_with_username_and_password(self, handle_server_url, username, password, **config):
        raise NotImplementedError()

    def instantiate_for_read_access(self, handle_server_url=None, **config):
        raise NotImplementedError()

    def instantiate_for_read_and_search(self, handle_server_url, reverselookup_username, reverselookup_password,
                                        **config):
        raise NotImplementedError()

    def instantiate_with_credentials(self, credentials, **config):
        raise NotImplementedError()

    def register_handle(self, handle, url, overwrite=False, **args):
        raise NotImplementedError()

    def add_admin_entry(self, handle, admin_handle, admin_handle_index, perm):
        raise NotImplementedError()

    def get_query_from_user(self, query):
        raise NotImplementedError()

    def convert_hs_admin_values_to_hex(self, handle):
        raise NotImplementedError()

    def create_batch_file(self, overwrite=False):
        raise NotImplementedError()

    def authenticate_seckey(self, user, password):
        raise NotImplementedError()

    def authenticate_pubkey(self, user, priv_key_path, passphrase=None):
        raise NotImplementedError()

    def search_handle(self, pattern=None, **args):
        raise NotImplementedError()

    def search_handle_multiple_keys(self, **args):
        raise NotImplementedError()


    @classmethod
    def check_client(cls, client):
        return client == cls.HANDLE_CLIENT
