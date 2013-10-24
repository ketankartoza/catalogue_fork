function zebraTables()
{
  $("table tr:even").addClass("even");
  $("table tr:odd").addClass("odd");
}

function loadContent( theUrl )
{
  uiBlock();
  $("#main-content").load( theUrl ,"",uiUnblock);
}

function loadSummaryTable(theId)
{
  uiBlock();
  $("#main-content").load("/sensorSummaryTable/" + theId + "/","",uiUnblock);
}

function uiBlock() {
    $.blockUI({
        message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
        css: {
            border: '1px solid #000',
            background: 'rgba(0, 0, 0, 0.3)',
            width: '550px',
            height:'550px'
        }
    });
}

function uiUnblock() {
    $.unblockUI();
}