function tree(select_id, display_file) {
  console.log("** Hi~ Inside the tree !!!")
  var screen_width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
  var margin = {
      top: 20,
      right: 120,
      bottom: 20,
      left: 120
  },
  width = screen_width - margin.right - margin.left,
      height = 800 - margin.top - margin.bottom;

  var i = 0,
      duration = 750,
      root;

  var tree = d3.layout.tree()
      .size([height, width]);

  var diagonal = d3.svg.diagonal()
      .projection(function (d) {
      return [d.y, d.x];
  });

  var svg = d3.select(select_id).append("svg")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "-200 0 2250 750")
      .append("g")

  d3.json(display_file, function(error, tree_data) {
    root = tree_data;
    console.log("@@ root: ", root)
    root.x0 = height / 2;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    console.log("** root: ", root)
    update(root);
  });

  d3.select(self.frameElement).style("height", "800px");

  function update(source) {

      // Compute the new tree layout.
      var nodes = tree.nodes(root).reverse(),
          links = tree.links(nodes);

      // Normalize for fixed-depth.
      nodes.forEach(function (d) {
          d.y = d.depth * 350;
      });

      // Update the nodes…
      var node = svg.selectAll("g.node")
          .data(nodes, function (d) {
          return d.id || (d.id = ++i);
      });

      // Enter any new nodes at the parent's previous position.
      var nodeEnter = node.enter().append("g")
          .attr("class", "node")
          .attr("transform", function (d) {
          return "translate(" + source.y0 + "," + source.x0 + ")";
      })
          .on("click", click);

      nodeEnter.append("circle")
          .attr("r", 1e-6)
          .style("fill", function(d) { return d.color; });

      nodeEnter.append("text")
          .attr("x", function (d) {
            if (d.children || d._children || d.name.includes("Person")) {
              position = -14;
            } else {
              position = 13;
            }
          return position;
        })
          .attr("dy", ".35em")
          .attr("text-anchor", function (d) {
            if (d.children == undefined && !d.name.includes("Person")) {
              position = "start";
            } else if (d.name.includes("Person")) {
              position = "end";
            } else {
              position = "end";
            }
            if (d.parent == "null") {
              position = "middle";
            }
            return position
        })
        .attr("dy", function (d) {
          if (d.children == undefined && !d.name.includes("Person")) {
            position = ".35em";
          } else if (d.name.includes("Person")) {
            position = "-0.5em";
          } else {
            position = ".35em";
          }
          if (d.parent == "null") {
            position = "-1em";
          }
          return position
        })
        .attr("dx", function (d) {
          if (d.children == undefined) {
            position = "0em";
          } else {
            position = "0em";
          }
          if (d.parent == "null") {
            position = "-3em";
          }
          return position
        })

          .style("fill-opacity", 1e-6)
          .text(function (d) {
          return d.name;
        })
          .attr("vector-effect", "non-scaling-stroke")
          .style("border", "red")
          .attr("fill", function (d) {
            if (d.children == undefined) {
              color = "#4287f5";
            } else {
              color = "#00298f";
            }
            if (d.name.includes("Person")) {
              color = "#9529c4";
            }
            if (d.name.includes("Infected")) {
              color = "#fc7303";
            }
            if (d.name.includes("Not infected")) {
              color = "#44ab00";
            }
            if (d.name.includes("Death")) {
              color = "red";
            }
            if (d.name.includes("Death")) {
              color = "red";
            }
            if (d.name.includes("Recovery")) {
              color = "green";
            }
          return color;
        })
          .style("font-size", function (d) {
            if (d.children == undefined && !d.name.includes("Person")) {
              size = 15;
            } else if (d.name.includes("Person")) {
              size = 30;
            } else {
              size = 23;
            }
            if (d.name.includes("Infected")) {
              size = 23;
            }
          return size;
        });

      // Transition nodes to their new position.
      var nodeUpdate = node.transition()
          .duration(duration)
          .attr("transform", function (d) {
          return "translate(" + d.y + "," + d.x + ")";
      });

      nodeUpdate.select("circle")
          .attr("r", function(d) { return (d.children == undefined || d.parent == "null") ? 10 : 5;} ) //function(d) { return d._children.length == 0 ? 3 : 10;}
          .style("fill", function(d) { return d.color; });

      nodeUpdate.select("text")
          .style("fill-opacity", 1);

      // Transition exiting nodes to the parent's new position.
      var nodeExit = node.exit().transition()
          .duration(duration)
          .attr("transform", function (d) {
          return "translate(" + source.y + "," + source.x + ")";
      })
          .remove();

      nodeExit.select("circle")
          .attr("r", 1e-6);

      nodeExit.select("text")
          .style("fill-opacity", 1e-6);

      // Update the links…
      var link = svg.selectAll("path.link")
          .data(links, function (d) {
          return d.target.id;
      });

      // Enter any new links at the parent's previous position.
      link.enter().insert("path", "g")
          .attr("class", "link")
          .attr("d", function (d) {
          var o = {
              x: source.x0,
              y: source.y0
          };
          return diagonal({
              source: o,
              target: o
          });
      });


      // Transition links to their new position.
      link.transition()
          .duration(duration)
          .attr("d", diagonal);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition()
          .duration(duration)
          .attr("d", function (d) {
          var o = {
              x: source.x,
              y: source.y
          };
          return diagonal({
              source: o,
              target: o
          });
      })
          .remove();

      // Update the link text
      var linktext = svg.selectAll("g.link")
          .data(links, function (d) {
          return d.target.id;
      });

      linktext.enter()
          .insert("g")
          .attr("class", "link")
          .append("text")
          .attr("x", "-65px")
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          // .attr("transform", function (d,i)
          //    {return "skewX(" + -25 + ")"; })
          .text(function (d) {
            return d.target.pb;
          })

      linktext.transition()
          .duration(duration)
          .attr("transform", function (d) {
          return "translate(" + ((d.source.y + d.target.y) / 2) + "," + ((d.source.x + d.target.x) / 2) + ")";
      })

      //Transition exiting link text to the parent's new position.
      linktext.exit().transition()
          .remove();


      // Stash the old positions for transition.
      nodes.forEach(function (d) {
          d.x0 = d.x;
          d.y0 = d.y;
      });
  }
  // Toggle children on click.
  function click(d) {
      if (d.children) {
          d._children = d.children;
          d.children = null;
      } else {
          d.children = d._children;
          d._children = null;
      }
      update(d);
  }
}
