// eslint-disable-next-line no-unused-vars
/* global chrome */

chrome.runtime.onInstalled.addListener(() =>
  chrome.contextMenus.create({
    title: 'Yagna text classify',
    id: 'yagna-service-poc',
    contexts: ['all'],
  }),
);

let windowId;

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (tab && info.menuItemId === 'yagna-service-poc') {
    if (!info.selectionText) alert('Select some text');
    else {
      if (windowId) chrome.windows.remove(windowId);

      chrome.windows.create(
        {
          url: 'popup.html',
          type: 'popup',
          width: 560,
          height: 280,
          left: screen.width - 560,
          top: 0,
        },
        (window) => {
          chrome.storage.local.set({ text: info.selectionText ? info.selectionText.trim() : '' });
          windowId = window.id;
        },
      );
    }
  }
});
