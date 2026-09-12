// VoxBox - Build Configuration
const { build } = require('electron-builder');

const config = {
  appId: 'com.voxbox.app',
  productName: 'VoxBox',
  directories: {
    output: 'release',
    buildResources: 'icons'
  },
  files: [
    'main.js',
    'preload.js',
    'package.json',
    'ui/**/*',
    'python/**/*',
    'requirements.txt'
  ],
  extraResources: [
    {
      from: 'requirements.txt',
      to: 'requirements.txt'
    }
  ],
  win: {
    target: 'nsis',
    icon: 'icons/icon.ico',
    artifactName: 'VoxBox-Setup-${version}.exe'
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
    installerIcon: 'icons/icon.ico',
    uninstallerIcon: 'icons/icon.ico'
  },
  mac: {
    target: 'dmg',
    icon: 'icons/icon.icns',
    category: 'public.app-category.productivity'
  },
  linux: {
    target: ['AppImage', 'deb'],
    icon: 'icons/icon.png',
    category: 'Audio;Utility'
  }
};

async function buildApp() {
  console.log('Building VoxBox...');
  try {
    await build({
      config,
      publish: null
    });
    console.log('✓ Build complete!');
    console.log('Check the release/ directory for installers.');
  } catch (error) {
    console.error('✗ Build failed:', error);
    process.exit(1);
  }
}

buildApp();
