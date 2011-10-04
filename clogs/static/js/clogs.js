(function() {
  var EPOCHS, MONTHS, SLIDE_DURATION, coverage_data, make_graph, options, relative_date, slide;
  EPOCHS = [["second", 1000], ["minute", 60 * 1000], ["hour", 60 * 60 * 1000], ["day", 24 * 60 * 60 * 1000], ["month", 30.4 * 24 * 60 * 60 * 1000], ["year", 12 * 30.4 * 24 * 60 * 60 * 1000]];
  MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  relative_date = function(date) {
    var difference, epoch, last, now, num, plural, time, _i, _len, _ref;
    now = (new Date()).getTime();
    difference = Math.abs(now - date);
    if (difference < EPOCHS[0][1]) {
      return "now";
    } else {
      last = EPOCHS[0];
    }
    _ref = EPOCHS.slice(1, EPOCHS.length);
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      epoch = _ref[_i];
      num = Math.round(difference / last[1]);
      if ((last[1] <= difference && difference <= epoch[1])) {
        break;
      } else {
        last = epoch;
      }
    }
    plural = num !== 1 ? "s" : "";
    time = now > date ? " ago" : " from now";
    return num + " " + last[0] + plural + time;
  };
  $.plot.formatDate = function(date, formatString, monthNames) {
    return relative_date(date);
  };
  coverage_data = function(clogs) {
    var clog, data, date, dta, file, lbl, name, _i, _j, _len, _len2, _ref, _results;
    data = {};
    for (_i = 0, _len = clogs.length; _i < _len; _i++) {
      clog = clogs[_i];
      date = clog["date"];
      _ref = clog["coverage"];
      for (_j = 0, _len2 = _ref.length; _j < _len2; _j++) {
        file = _ref[_j];
        name = file["name"];
        if (!(data[name] != null)) {
          data[name] = [];
        }
        data[name].push([date, parseInt(file["percent_coverage"])]);
      }
    }
    _results = [];
    for (lbl in data) {
      dta = data[lbl];
      _results.push({
        label: lbl,
        data: dta
      });
    }
    return _results;
  };
  options = function(legend_selector) {
    return {
      colors: ["#0A3A4A", "#196674", "#33A6B2", "#9AC836", "#D0E64B"],
      grid: {
        borderWidth: 0,
        clickable: true,
        hoverable: true,
        labelMargin: 30,
        markings: []
      },
      legend: {
        container: legend_selector,
        noColumns: 3
      },
      selection: {
        mode: "xy"
      },
      series: {
        lines: {
          show: true
        },
        points: {
          show: true
        },
        threshold: {
          below: 95,
          color: "#E65042"
        }
      },
      xaxis: {
        mode: "time",
        monthNames: MONTHS,
        tickLength: 5
      },
      yaxis: {
        max: 100,
        position: "right"
      }
    };
  };
  make_graph = function(selector) {
    var data;
    data = $.parseJSON(json_clogs);
    return $.plot($(selector), coverage_data(data), options("#graph-legend"));
  };
  SLIDE_DURATION = 500;
  slide = function(slider, slide_in, slide_over, width) {
    var shift;
    $(slide_in).css("width", width);
    shift = width - 60;
    return $(slider).click(function() {
      if ($(slide_in).is(":visible")) {
        $(slide_over).animate({
          left: "+=" + shift
        });
        return $(slide_in).hide(SLIDE_DURATION);
      } else {
        $(slide_in).show(SLIDE_DURATION);
        return $(slide_over).animate({
          left: "-=" + shift
        });
      }
    });
  };
  $(document).ready(function() {
    make_graph("#graph");
    return slide("#settings-toggle", "#settings", "#content", 450);
  });
}).call(this);
