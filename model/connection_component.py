from influxdb_client import InfluxDBClient

class InfluxDBConnection:
    def __init__(self):
        """Inicializa la conexión usando las credenciales locales."""
        self.url = "http://192.168.145.164:8086"
        self.token = "2mLHE8EitguD8XEZT-Sw-0_aks6W4g2vUupNzWoSh7sGYKfOAOCThuioHFb0Zs6U2lPNrWIo42L1BTsFtQM4Ew=="
        self.org = "jkgh"
        self.bucket = "jkgh"

    def get_client(self):
        return InfluxDBClient(url=self.url, token=self.token, org=self.org)

    def get_write_api(self, client):
        return client.write_api()

    def get_query_api(self, client):
        return client.query_api()
