
function selectionClick(info, tab){
    text = info["selectionText"];
    chrome.windows.create({url: "./new.html?text="+text, type: "popup", width: 900, height: 600});
}
function openNew(info, tab){
    chrome.windows.create({url: "./new.html", type: "popup", width: 900, height: 900});
}
function openAll(info, tab){
    chrome.windows.create({url: "./all.html", type: "popup", width: 900, height: 600});
}

chrome.contextMenus.create({"title": 'Criar lembrete', "contexts":["selection"], "onclick": selectionClick});

chrome.contextMenus.create({"title": "Todos os lembretes", "onclick":openAll});
chrome.contextMenus.create({"title": "Novo Lembrete...", "onclick":openNew});
