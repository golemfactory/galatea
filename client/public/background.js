// eslint-disable-next-line no-unused-vars
/* global chrome */

chrome.runtime.onInstalled.addListener(() =>
  chrome.contextMenus.create({
    title: 'Galatea, analyze!',
    id: 'galatea',
    contexts: ['all'],
  }),
);

let windowId;

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (tab && info.menuItemId === 'galatea') {
    const createPopup = () =>
      chrome.windows.create(
        {
          url: 'popup.html',
          type: 'popup',
          width: 357,
          height: 800,
          left: screen.width - 357,
          top: 0,
        },
        (window) => {
          chrome.storage.local.set({ text: info.selectionText ? info.selectionText.trim() : '' });
          windowId = window.id;
        },
      );

    return chrome.windows.getAll({ windowTypes: ['popup'] }, (window) =>
      window.length === 0 ? createPopup() : chrome.windows.remove(windowId, createPopup()),
    );
  }
});
