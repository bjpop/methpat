(function() {
  var out$ = typeof exports != 'undefined' && exports || this;

  var doctype = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">';

  function isExternal(url) {
    return url && url.lastIndexOf('http',0) == 0 && url.lastIndexOf(window.location.host) == -1;
  }

  function inlineImages(callback) {
    var images = document.querySelectorAll('svg image');
    var left = images.length;
    if (left == 0) {
      callback();
    }
    for (var i = 0; i < images.length; i++) {
      (function(image) {
        var href = image.getAttribute('xlink:href');
        if (href) {
          if (isExternal(href.value)) {
            console.warn("Cannot render embedded images linking to external hosts.");
            return;
          }
        }
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var img = new Image();
        href = href || image.getAttribute('href');
        img.src = href;
        img.onload = function() {
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);
          image.setAttribute('xlink:href', canvas.toDataURL('image/png'));
          left--;
          if (left == 0) {
            callback();
          }
        }
        img.onerror = function() {
          console.log("Could not load "+href);
          left--;
          if (left == 0) {
            callback();
          }
        }
      })(images[i]);
    }
  }

  function styles(dom) {
    var css = "";
    var sheets = document.styleSheets;
    for (var i = 0; i < sheets.length; i++) {
      if (isExternal(sheets[i].href)) {
        console.warn("Cannot include styles from other hosts.");
        continue;
      }
      var rules = sheets[i].cssRules;
      if (rules != null) {
        for (var j = 0; j < rules.length; j++) {
          var rule = rules[j];
          if (typeof(rule.style) != "undefined") {
            css += rule.selectorText + " { " + rule.style.cssText + " }\n";
          }
        }
      }
    }

    var s = document.createElement('style');
    s.setAttribute('type', 'text/css');
    s.innerHTML = "<![CDATA[\n" + css + "\n]]>";

    var defs = document.createElement('defs');
    defs.appendChild(s);
    return defs;
  }

  out$.svgAsDataUri = function(el, scaleFactor, cb) {
    scaleFactor = scaleFactor || 1;

    inlineImages(function() {
      var outer = document.createElement("div");
      var clone = el.cloneNode(true);
      var width = parseInt(
        clone.getAttribute('width')
          || clone.style.width
          || out$.getComputedStyle(el).getPropertyValue('width')
      );
      var height = parseInt(
        clone.getAttribute('height')
          || clone.style.height
          || out$.getComputedStyle(el).getPropertyValue('height')
      );

      var xmlns = "http://www.w3.org/2000/xmlns/";

      clone.setAttribute("version", "1.1");
      clone.setAttributeNS(xmlns, "xmlns", "http://www.w3.org/2000/svg");
      clone.setAttributeNS(xmlns, "xmlns:xlink", "http://www.w3.org/1999/xlink");
      clone.setAttribute("width", width * scaleFactor);
      clone.setAttribute("height", height * scaleFactor);
      clone.setAttribute("viewBox", "0 0 " + width + " " + height);
      outer.appendChild(clone);

      clone.insertBefore(styles(clone), clone.firstChild);

      var svg = doctype + outer.innerHTML;
      var uri = 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(svg)));
      if (cb) {
        cb(uri);
      }
    });
  }

  out$.saveSvgAsPng = function(el, name, scaleFactor) {
    out$.svgAsDataUri(el, scaleFactor, function(uri) {
      var image = new Image();
      image.src = uri;
      image.onload = function() {
        var canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext('2d');
        context.drawImage(image, 0, 0);

        var a = document.createElement('a');
        a.download = name;
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
      }
    });
  }
})();
