EPOCHS = [
    ["second",                            1000]
    ["minute",                       60 * 1000]
    ["hour"  ,                  60 * 60 * 1000]
    ["day"   ,             24 * 60 * 60 * 1000]
    ["month" ,      30.4 * 24 * 60 * 60 * 1000]
    ["year"  , 12 * 30.4 * 24 * 60 * 60 * 1000]
]


MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


relative_date = (date) ->
    now = (new Date()).getTime()
    difference = Math.abs(now - date)

    if difference < EPOCHS[0][1]
        return "now"
    else
        last = EPOCHS[0]

    for epoch in EPOCHS[1...EPOCHS.length]
        num = Math.round(difference / last[1])

        if last[1] <= difference <= epoch[1]
            break
        else
            last = epoch

    plural = if num != 1 then "s" else ""
    time = if now > date then " ago" else " from now"
    num + " " + last[0] + plural + time


$.plot.formatDate = (date, formatString, monthNames) -> relative_date(date)


coverage_data = (clogs) ->
    data = {}

    for clog in clogs
        date = clog["date"]

        for file in clog["coverage"]
            name = file["name"]
            data[name] = [] if not data[name]?
            data[name].push([date, parseInt(file["percent_coverage"])])

    {label : lbl, data : dta} for lbl, dta of data


options = (legend_selector) -> {

    colors : ["#0A3A4A", "#196674", "#33A6B2", "#9AC836", "#D0E64B"]

    grid : {
        borderWidth : 0
        clickable : true
        hoverable : true
        labelMargin : 30
        markings : []
    }

    legend : {
        container : legend_selector
        noColumns : 3
    }

    selection : {
        mode : "xy"
    }

    series : {
        lines : {
            show : true
        }

        points : {
            show : true
        }

        threshold : {
            below : 95
            color : "#E65042"
        }
    }

    xaxis : {
        mode : "time"
        monthNames : MONTHS
        tickLength : 5
    }

    yaxis : {
        max : 100
        position : "right"
    }
}


make_graph = (selector) ->
    data = $.parseJSON(json_clogs)
    $.plot($(selector), coverage_data(data), options("#graph-legend"))


SLIDE_DURATION = 500


slide = (slider, slide_in, slide_over, width) ->
    $(slide_in).css("width", width)

    shift = width - 60  # XXX: Hey cool a magic constant.

    $(slider).click( ->
        if $(slide_in).is(":visible")

            $(slide_over).animate({
                left : "+=#{shift}"
            })
            $(slide_in).hide(SLIDE_DURATION)
        else
            $(slide_in).show(SLIDE_DURATION)
            $(slide_over).animate({
                left : "-=#{shift}"
            })
    )


$(document).ready( ->
    make_graph("#graph")
    slide("#settings-toggle", "#settings", "#content", 450)
)
