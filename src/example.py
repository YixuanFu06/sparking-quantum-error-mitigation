import tensorcircuit as tc
from tensorcircuit.cloud import apis


token = 'W6QyiJRRS.DFibko9DVIuZwdqoTa5mGtl8HxoIYy4pfCPMTwhBztGrnXovVzUT0L6c-7nilqVxg1lcWd7Fj0pmLHvmb9RmA8TD8fSndBorSlfdVxPcJRQuKs.R5M9Ecu6G5DyJaAPwULZPs5r6H23G8='
apis.set_token(token)
print(apis.list_devices(provider="tencent"))



if __name__ == "__main__":
    shots = 4096
    c = tc.Circuit(2)
    c.x(0)
    c.cx(0,1)
    ts = apis.submit_task(provider="tencent", device='tianji_s2?o=3', circuit=c, shots=shots)
    data = ts.results()
    print(data)