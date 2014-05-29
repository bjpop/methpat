import json

def make_html(args, json_dict):
    js_strings = []
    for amplicon, amplicon_dict in json_dict.items():
        # sort patterns on count in descending order
        amplicon_dict['patterns'].sort(key=lambda x:x['count'], reverse=True)
        json_str = json.dumps(amplicon_dict)
        js_strings.append('create_matrix({});'.format(json_str))
    doc = DOC_TEMPLATE % '\n'.join(js_strings)
    with open(args.html, 'w') as html_file:
        html_file.write(doc)

DOC_TEMPLATE = '''
<!DOCTYPE html>
<meta charset="utf-8">
<title>Methylation patterns</title>
<style>

@import url(style.css);

.background {
  fill: #eee;
}

line {
  stroke: #fff;
  stroke-opacity: .5;
  shape-rendering: crispEdges;
}

textarea {
  padding: 2px;
  width: 714px;
  height: 360px;
}

</style>

<h1>Methylation Patterns</h1>

<script src="d3.v3.min.js"></script>
<script>

function create_matrix(data) {

   var patterns = data.patterns;
   var num_patterns = patterns.length;

   if (num_patterns == 0)
      return;

   var num_sites = patterns[0].methylation.length

   var margin = {top: 0, right: 0, bottom: 0, left: 0};

   var heading = d3.select("body").append("h3");
   heading.text(data.amplicon + ' ' + data.chr + ' ' + data.start + ':' + data.end)

   // Compute the maximum, minimum and total counts for all the data.
   var max_count = -1, min_count = -1, total_count = 0;
   for (i = 0; i < num_patterns; i++)
   {
      this_count = patterns[i].count;
      total_count += this_count;
      if (min_count == -1 || this_count < min_count)
      {
         min_count = this_count;
      }
      if (max_count == -1 || this_count > max_count)
      {
         max_count = this_count;
      }
   } 

   var max_proportion = max_count / total_count;
   var min_proportion = min_count / total_count;

   var cell_width = 10;
   var cell_height = cell_width;
   var width = num_sites * cell_width;

   var patterns_height = num_sites * cell_height;
   var counts_height = 50;
   var gap = 10;

   var img_width = num_patterns * cell_width;
   var img_height = patterns_height + gap + counts_height;

   var cell_y = d3.scale.ordinal()
           .domain(d3.range(num_sites))
           .rangeBands([0, patterns_height]);

   var mag_scale = d3.scale.log()
         .domain([min_count, max_count])
         .range([0.2, 0.7]);

   var count_bar_scale = d3.scale.log()
         .domain([min_proportion, max_proportion])
         .range([1, counts_height]);

   var patterns_svg = d3.select("body").append("svg")
      .attr("height", img_height)
      .attr("width", img_width);

   var columns = patterns_svg.selectAll(".column")
       .data(patterns)
       .enter().append("g")
       .attr("class", "column")
       // translate the column in the x direction (shift it across the page)
       .attr("transform", function(d, i) { return "translate(" + i * cell_width + ",0)"; });

   columns.selectAll(".cell")
       .data(function(d) {
           values = [];
           for (i = 0; i < num_sites; i++)
           {
               var cell_val = { meth_state : d.methylation[i], count : d.count }
               values.push(cell_val);
           }
           return values.reverse();
       })
       .enter().append("rect")
       .attr("class", "cell")
       // shift the row down by the cell height
       .attr("y", function(d, i) { return cell_y(i); })
       .attr("width", cell_width)
       .attr("height", cell_height)
       .attr("stroke-width", 0.5)
       .attr("stroke", 'black')
       .attr("fill", function(d, i) {

           function make_colour(name, count) {
              var colour = d3.hsl(name);
              colour.l = mag_scale(count);
              return colour;
           }

           var meth_state = d.meth_state;

           if (meth_state == 0) {
              return make_colour('red', d.count);
           }
           else if (meth_state == 1) {
              return make_colour('yellow', d.count);
           } 
           else if (meth_state == 2) {
              return make_colour('blue', d.count);
           };
        })

    var count_bars = patterns_svg.selectAll(".count_bar")
       .data(patterns)
       .enter().append("rect")
       .attr("class", "count_bar")
       .attr("transform", function(d, i)
           { return "translate(" + i * cell_width + "," + (patterns_height + gap) + ")"; })
       .attr("class", "cell")
       .attr("width", cell_width)
       .attr("height", function(d, i) { return count_bar_scale(d.count/ total_count); })
       .attr("fill", 'green');
}

%s

</script>
'''
