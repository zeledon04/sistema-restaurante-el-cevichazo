function doSearch() {
    const tableReg = document.getElementById("datos");
    const searchText = document.getElementById("searchTerm").value.toLowerCase();
    let total = 0;

    for (let i = 1; i < tableReg.rows.length; i++) {
        if (tableReg.rows[i].classList.contains("noSearch")) {
            continue;
        }

        let found = false;
        const cellsOfRow = tableReg.rows[i].getElementsByTagName("td");

        for (let j = 0; j < cellsOfRow.length && !found; j++) {
            const compareWith = cellsOfRow[j].innerHTML.toLowerCase();
            if (searchText.length == 0 || compareWith.startsWith(searchText)) {
                found = true;
                total++;
            }
        }

        if (found) {
            tableReg.rows[i].style.display = "";
        } else {
            tableReg.rows[i].style.display = "none";
        }
    }

    const lastTR = tableReg.rows[tableReg.rows.length - 1];
    const td = lastTR.querySelector("td");
    lastTR.classList.remove("hide");

    if (searchText == "") {
        lastTR.classList.add("hide");
    }
    updateRowNumbers();
}

    function updateRowNumbers() {
        var table = document.getElementById('datos');
        var rows = table.getElementsByClassName('main-row');
        var counter = 1;

        for (var i = 0; i < rows.length; i++) {
            if (rows[i].style.display !== "none") {
                rows[i].getElementsByTagName('td')[0].innerText = counter;
                counter++;
            }
        }
    }