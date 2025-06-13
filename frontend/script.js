let currentPage = 1;
const limit = 10;
let currentQuery = "";
let totalPages = 1;
let currentSort = { field: null, direction: "asc" };

document.getElementById("searchButton").addEventListener("click", () => {
    currentPage = 1;
    performSearch();
});

document.getElementById("searchInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        currentPage = 1;
        performSearch();
    }
});

document.getElementById("pagination").addEventListener("click", (e) => {
    if (e.target.id === "prevPage" && currentPage > 1) {
        currentPage--;
        performSearch();
    } else if (e.target.id === "nextPage" && currentPage < totalPages) {
        currentPage++;
        performSearch();
    }
});

function performSearch() {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) return;
    currentQuery = query;

    const url = new URL("http://localhost:8000/search");
    url.searchParams.set("q", currentQuery);
    url.searchParams.set("page", currentPage);
    url.searchParams.set("limit", limit);

    if (currentSort.field) {
        url.searchParams.set("sort", currentSort.field);
        url.searchParams.set("order", currentSort.direction);
    }

    fetch(url)
        .then(res => res.json())
        .then(data => {
            renderResults(data.results);
            renderPagination(data.page, Math.ceil(data.total / data.limit));
            updateUrlParams(); // ✅ correctly placed inside .then
        })
        .catch(err => {
            console.error("Search error:", err);
        });
}

// Move this outside performSearch so it's not nested (optional but cleaner)
function updateUrlParams() {
    const params = new URLSearchParams();
    params.set("q", currentQuery);
    params.set("page", currentPage);
    if (currentSort.field) {
        params.set("sort", currentSort.field);
        params.set("order", currentSort.direction);
    }
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    history.pushState({}, "", newUrl);
}

function renderResults(results) {
    if (results.length === 0) {
        document.getElementById("results").innerHTML = "<p>No results found.</p>";
        return;
    }

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headers = [
    { label: "Title", field: "title" },
    { label: "Creators", field: "creators" },
    { label: "Publication", field: "publication" },
    { label: "Date", field: "date" },
    { label: "DOI", field: "doi" }
];

    const headerRow = document.createElement("tr");
headers.forEach(header => {
    const th = document.createElement("th");
    const isSortable = ["title", "creators", "publication", "date"].includes(header.field);
    th.style.cursor = isSortable ? "pointer" : "default";

    let arrow = "";
    if (currentSort.field === header.field) {
        arrow = currentSort.direction === "asc" ? " ▲" : " ▼";
    } else if (isSortable) {
        arrow = " ⇅"; // neutral sort indicator
    }

    th.textContent = header.label + arrow;

    if (isSortable) {
        th.onclick = () => sortBy(header.field);
    }

    headerRow.appendChild(th);
});
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    results.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.title || ""}</td>
            <td>${item.creators || ""}</td>
            <td>${item.publication || ""}</td>
            <td>${item.date || ""}</td>
            <td><a href="${item.DOI ? `https://doi.org/${item.DOI}` : '#'}" target="_blank">${item.DOI || ""}</a></td>
        `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    document.getElementById("results").innerHTML = "";
    document.getElementById("results").appendChild(table);
}

function renderPagination(page, total) {
    totalPages = total;
    const container = document.getElementById("pagination");
    container.innerHTML = `
        <button id="prevPage" ${page === 1 ? "disabled" : ""}>Previous</button>
        <span>Page ${page} of ${total}</span>
        <button id="nextPage" ${page === total ? "disabled" : ""}>Next</button>
    `;
}

function sortBy(field) {
    const newDirection =
        currentSort.field === field && currentSort.direction === "asc"
            ? "desc"
            : "asc";

    currentSort = { field, direction: newDirection };
    currentPage = 1;
    performSearch();
}