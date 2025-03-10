import pyvis

# function to add click event to html generated by pyvis
def insert_click_event_js(graph):

    # Inject JavaScript to capture click events
    click_js = """
    <script type="text/javascript">
        // let's create a real unique tag to locate this in the html
        network.on("click", function(params) {
            if (params.nodes.length > 0) {
                let clickedNode = params.nodes[0];
                fetch('/clicked_node', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ node: clickedNode })
                });
            }
        });
    </script>
    """

    # save the graph as html
    graph_file = "pre_click_graph.html"
    graph.save_graph(graph_file)

    # insert javascript for the click event
    with open(graph_file, "r", encoding="utf-8") as f:
        post_click_graph = f.read().replace("</body>", click_js + "</body>")  # Inject JS

    print("complete")

    return post_click_graph