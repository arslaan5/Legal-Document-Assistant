from langchain.callbacks.base import BaseCallbackHandler

class CustomLogger(BaseCallbackHandler):
    def on_chain_start(self, chain, inputs, **kwargs):
        print(f"Chain started: {chain}")
        print(f"Inputs: {inputs}")

    def on_chain_end(self, outputs, **kwargs):
        print(f"Chain ended. Outputs: {outputs}")

    def on_tool_start(self, tool, input_str, **kwargs):
        print(f"Tool started: {tool} with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"Tool ended with output: {output}")

