// Import any necessary dependencies
const fetch = require('node-fetch');

// Import the functions to be tested
const { sendData, showAmounts, checkImageSize } = require('../backend/static/webscripts.js');

// Mock the necessary DOM elements
const mockParkingInput = { value: '123' };
const mockAccParkInput = { value: '456' };
const mockImagePickerInput = { files: [{ name: 'image.jpg' }] };

// Mock the necessary global objects and methods
global.document = {
  getElementById: jest.fn((id) => {
    if (id === 'number1') return mockParkingInput;
    if (id === 'number2') return mockAccParkInput;
    if (id === 'imagePicker') return mockImagePickerInput;
  }),
};

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ success: true }),
  })
);

global.sessionStorage = {
  setItem: jest.fn(),
  getItem: jest.fn((key) => (key === 'parking' ? '1' : '2')),
};

global.window = {
  location: {
    href: '',
  },
};

global.alert = jest.fn();

global.Image = jest.fn(() => ({
  onload: null,
  src: null,
}));

global.FileReader = jest.fn(() => ({
  onload: null,
  readAsDataURL: jest.fn(),
}));

describe('sendData', () => {
  it('should send data correctly', () => {
    sendData();

    expect(fetch).toHaveBeenCalledWith('/save_spots', expect.anything());
    expect(sessionStorage.setItem).toHaveBeenCalledWith('parking', '123');
    expect(sessionStorage.setItem).toHaveBeenCalledWith('accPark', '456');
  });
});

describe('showAmounts', () => {
  it('should show amounts correctly', () => {
    document.body.innerHTML = `
      <div id="park"></div>
      <div id="acc"></div>
    `;

    showAmounts();

    expect(document.getElementById('park').innerHTML).toBe('1');
    expect(document.getElementById('acc').innerHTML).toBe('2');
  });
});

describe('checkImageSize', () => {
  it('should check image size correctly', () => {
    const mockFile = new File([''], 'filename', { type: 'image/png' });
    const mockInput = {
      files: {
        0: mockFile,
        length: 1,
        item: () => mockFile
      },
      value: 'initial value',
    };

    checkImageSize(mockInput);

    const mockImage = new Image();
    const mockReader = new FileReader();

    mockReader.onload({ target: { result: 'data:image/png;base64,' } });
    mockImage.onload();

    expect(alert).toHaveBeenCalledWith('Please select an image of size 3840x2160.');
    expect(mockInput.value).toBe('');
  });
});
