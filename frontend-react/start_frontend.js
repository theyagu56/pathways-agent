#!/usr/bin/env node
/**
 * Helper script to start the React frontend with better error handling
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function checkEnvironment() {
    console.log('🔍 Checking React frontend environment...');
    
    // Check current directory
    const currentDir = process.cwd();
    console.log(`📁 Current directory: ${currentDir}`);
    
    // Check if we're in the right place
    const packageJsonPath = path.join(currentDir, 'package.json');
    if (!fs.existsSync(packageJsonPath)) {
        console.log('❌ package.json not found in current directory');
        console.log('💡 Make sure you\'re in the frontend-react directory');
        return false;
    }
    
    // Check package.json
    try {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        console.log(`✅ Found package.json: ${packageJson.name} v${packageJson.version}`);
    } catch (e) {
        console.log('❌ Error reading package.json:', e.message);
        return false;
    }
    
    // Check if node_modules exists
    const nodeModulesPath = path.join(currentDir, 'node_modules');
    if (!fs.existsSync(nodeModulesPath)) {
        console.log('❌ node_modules not found');
        console.log('💡 Please run: npm install');
        return false;
    }
    console.log('✅ node_modules found');
    
    // Check for React dependencies
    const reactPath = path.join(nodeModulesPath, 'react');
    if (!fs.existsSync(reactPath)) {
        console.log('❌ React not found in node_modules');
        console.log('💡 Please run: npm install');
        return false;
    }
    console.log('✅ React found');
    
    // Check environment variables
    const hostEnv = process.env.HOST;
    if (hostEnv && hostEnv !== 'localhost' && hostEnv !== '127.0.0.1') {
        console.log(`⚠️  HOST environment variable is set to: ${hostEnv}`);
        console.log('💡 This might cause issues. Consider unsetting it: unset HOST');
    } else {
        console.log('✅ HOST environment variable is properly set or not set');
    }
    
    // Check if port 3000 is available
    try {
        execSync('lsof -ti:3000', { stdio: 'ignore' });
        console.log('⚠️  Port 3000 is already in use');
        console.log('💡 You may need to stop the existing process or use a different port');
    } catch (e) {
        console.log('✅ Port 3000 is available');
    }
    
    return true;
}

function startFrontend() {
    if (!checkEnvironment()) {
        console.log('❌ Environment check failed. Please fix the issues above.');
        process.exit(1);
    }
    
    console.log('\n🚀 Starting React frontend...');
    console.log('=' * 50);
    
    // Unset problematic HOST variable for this process
    if (process.env.HOST && process.env.HOST !== 'localhost') {
        console.log('🔧 Unsetting HOST environment variable for this session...');
        delete process.env.HOST;
    }
    
    // Set proper environment variables
    const env = {
        ...process.env,
        HOST: 'localhost',
        PORT: '3000',
        BROWSER: 'none' // Prevent auto-opening browser
    };
    
    try {
        console.log('📦 Starting React development server...');
        console.log('🌐 Frontend will be available at: http://localhost:3000');
        console.log('🔗 Backend should be running at: http://localhost:8000');
        console.log('💡 Press Ctrl+C to stop the server');
        console.log('=' * 50);
        
        const child = spawn('npm', ['start'], {
            stdio: 'inherit',
            env: env,
            shell: true
        });
        
        child.on('error', (error) => {
            console.error('❌ Error starting React app:', error.message);
            process.exit(1);
        });
        
        child.on('close', (code) => {
            if (code !== 0) {
                console.error(`❌ React app exited with code ${code}`);
                process.exit(code);
            }
        });
        
        // Handle process termination
        process.on('SIGINT', () => {
            console.log('\n🛑 Stopping React frontend...');
            child.kill('SIGINT');
        });
        
        process.on('SIGTERM', () => {
            console.log('\n🛑 Stopping React frontend...');
            child.kill('SIGTERM');
        });
        
    } catch (error) {
        console.error('❌ Error starting React app:', error.message);
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    startFrontend();
}

module.exports = { checkEnvironment, startFrontend }; 