function createGraph(jsonData) {
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 900 - margin.left - margin.right,
        height = 800 - margin.top - margin.bottom;

// append the div object to the body of the page
    var div = d3.select("#my_dataviz")
        //.append("div")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    // Initialize the links
    var link = div
        .selectAll("line")
        .data(jsonData.links)
        .enter()
        .append("line")
        .style("stroke", "#aaa")

    // Initialize the nodes
    var node = div
        .selectAll("circle")
        .data(jsonData.nodes)
        .enter()
        .append("circle")
        .attr("r", 20)
        .style("fill", function (n) {
            console.log(n.type)
            switch (n.type) {
                case "Junction":
                    return "#186aed"
                case "Tank":
                    return "#7fed18"
                case "Valve":
                    return "#07f59a"
                case "Pipe":
                    return "#ccb927"
                case "Pump":
                    return "#cc2727"
                case "Reservoir":
                    return "#db6516"
                default:
                    return "#8e07f5"
            }
        })
    var text = div.selectAll("p")
        .data(jsonData.nodes)
        .enter()
        .append("p")
        .text("text")

    // Let's list the force we wanna apply on the network
    var simulation = d3.forceSimulation(jsonData.nodes)                 // Force algorithm is applied to data.nodes
        .force("link", d3.forceLink()                               // This force provides links between nodes
            .id(function (d) {
                return d.id;
            })                     // This provide  the id of a node
            .links(jsonData.links)                                    // and this the list of links
        )
        .force("charge", d3.forceManyBody().strength(-100))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
        .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the div area
        .on("end", ticked);

    // This function is run at each iteration of the force algorithm, updating the nodes position.
    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x + 6;
            })
            .attr("cy", function (d) {
                return d.y - 6;
            });
        text
            .attr("cx", function (d) {
                return d.x + 6;
            })
            .attr("cy", function (d) {
                return d.y - 6;
            });
    }


}
