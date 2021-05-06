// eslint-disable-next-line no-unused-vars
/* global chrome */

chrome.contextMenus.create({
  title: 'Yagna text classify',
  id: 'yagna-service-poc',
  contexts: ['all'],
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (tab && info.menuItemId === 'yagna-service-poc') {
    if (!info.selectionText) alert('Select some text');
    else return chrome.runtime.sendMessage(info.selectionText.trim());
  }
});
