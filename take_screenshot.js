const puppeteer = require('puppeteer');
var yargs = require('yargs');
const delay = require('delay');
const fs = require('fs');
const path = require('path');

let argv = yargs(process.argv.slice(2))
    .detectLocale(false)
    .usage('$0 [options] <url>', 'Take a screenshot of a webpage', (yargs) => {
        yargs
            .option('width', {
                description: 'Viewport width',
                type: 'number',
                demandOption: false,
                default: 1280,
            })
            .option('height', {
                description: 'Viewport height',
                type: 'number',
                demandOption: false,
                default: 720,
            })
            .option('outputDir', {
                description: 'Output directory, defaults to current directory',
                type: 'string',
                demandOption: false,
                default: '.',
            })
            .option('filename', {
                description: 'Filename of the produced screenshot',
                type: 'string',
                demandOption: false,
                default: 'screenshot',
            })
            .option('inputDir', {
                description: 'Input directory, defaults to current directory',
                type: 'string',
                demandOption: false,
                default: '.',
            })
            .option('userAgent', {
                description: 'User agent',
                type: 'string',
                demandOption: false,
                default: '',
            })
            .option('cookies', {
                description: 'Cookies in json format as string',
                type: 'string',
                demandOption: false,
                default: '',
            })
            .option('cookiesFile', {
                description: 'Path of the file containing the cookies',
                type: 'string',
                demandOption: false,
                default: '',
            })
            .option('delay', {
                description: 'Delay before taking the screenshot in ms',
                type: 'number',
                demandOption: false,
                default: 0,
            })
            .option('format', {
                description: 'Image format of the screenshot',
                type: 'string',
                choices: ['png', 'jpeg', 'webp'],
                demandOption: false,
                default: 'png',
            })
            .positional('url', {
                description:
                    'Url of the webpage you want to take a screenshot of',
                type: 'string',
            })
            .example(
                '$0 https://github.com',
                'Take a screenshot of https://github.com and save it as screenshot.png'
            )
            .example(
                '$0 --cookiesFile=cookies.json https://google.com',
                'Load the cookies from cookies.json, take a screenshot of https://google.com and save it as screenshot.png'
            );
    })
    .help('h')
    .alias('h', 'help')
    .version()
    .alias('version', 'v')
    .wrap(Math.min(yargs.terminalWidth(), 130)).argv;

takeScreenshot(argv);

function takeScreenshot(argv) {
    (async () => {
        const browser = await puppeteer.launch({
            defaultViewport: {
                width: argv.width,
                height: argv.height,
            },
            bindAddress: '0.0.0.0',
            args: [
                '--no-sandbox',
                '--headless',
                '--disable-gpu',
                '--disable-dev-shm-usage',
	        	'--ignore-certificate-errors',
                '--remote-debugging-port=9222',
                '--remote-debugging-address=0.0.0.0',
            ],
        });

        const page = await browser.newPage();

        if (argv.userAgent) await page.setUserAgent(argv.userAgent);

        if (argv.cookies) {
            let cookies = JSON.parse(argv.cookies);
            if (Array.isArray(cookies)) {
                await page.setCookie(...cookies);
            } else {
                await page.setCookie(cookies);
            }
        }

        if (argv.cookiesFile) {
            let cookies = JSON.parse(
                fs.readFileSync(path.join(argv.inputDir, argv.cookiesFile))
            );
            if (Array.isArray(cookies)) {
                await page.setCookie(...cookies);
            } else {
                await page.setCookie(cookies);
            }
        }
        try{
            await page.goto(argv.url, { waitUntil: 'networkidle0' });
        }
        catch(err){}
        
        if (argv.delay) await delay(argv.delay);

        await page.screenshot({
            path: path
                .join(argv.outputDir, argv.filename + '.' + argv.format)
                .toString(),
            type: argv.format,
        });

        await browser.close();
    })();
}
