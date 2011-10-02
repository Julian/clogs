(function() {
  var EPOCHS, MONTHS, options, relative_date;
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
  window.coverage_data = function(clogs) {
    var clog, coverage, data, date, dta, file, lbl, _i, _len, _ref, _results;
    data = {};
    for (_i = 0, _len = clogs.length; _i < _len; _i++) {
      clog = clogs[_i];
      date = clog["date"];
      _ref = clog["coverage"];
      for (file in _ref) {
        coverage = _ref[file];
        if (!(data[file] != null)) {
          data[file] = [];
        }
        data[file].push([date, coverage]);
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
  options = {
    colors: ["#0A3A4A", "#196674", "#33A6B2", "#9AC836", "#D0E64B"],
    grid: {
      borderWidth: 0,
      clickable: true,
      hoverable: true,
      labelMargin: 30,
      markings: []
    },
    selection: {
      mode: "x"
    },
    series: {
      lines: {
        show: true
      },
      points: {
        show: true
      }
    },
    xaxis: {
      mode: "time",
      monthNames: MONTHS,
      tickLength: 5,
      timeformat: "%b %d"
    },
    yaxis: {
      min: 0,
      max: 100,
      position: "right"
    }
  };
  window.bind_graph_to = function(selector) {
    var data;
    data = $.parseJSON(json_clogs);
    return $.plot($(selector), coverage_data(data), options);
  };
}).call(this);