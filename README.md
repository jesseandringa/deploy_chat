# chat_website
CASEY INSTRUCTIONS
cd into deploy_chat into terminal if not already
- 'cd deploy_chat'
run webscraper.
- from deploy chat folder in terminal run the following command
- 'python chat_server/chat/scraper/website_scraper.py'

to change counties
- in website_scraper search for casey
- follow example of names for folders and such
- for folder paths 
  - right click on folder on the left side.
  - click copy relative path
  - paste

to run in headless mode
- search for headless in website_scraper.py
- comment the headless line out (#)

to move pdfs that are out of place
- open up casey_move_pdfs.py
- look at comments i made you
- replace folder name with one you want them to end up in
- run 'python chat_server/chat/scraper/casey_move_pdfs.py'











Website chatbot to be hosted for individual investor use
ssh -i chatkeypair.pem ec2-user@3.143.1.57

node dependencies
"@fortawesome/free-solid-svg-icons": "^6.5.2",
    "@fortawesome/react-fontawesome": "^0.2.0",

    packagage-lock.json 2450

    "node_modules/@fortawesome/fontawesome-common-types": {
      "version": "6.5.2",
      "resolved": "https://registry.npmjs.org/@fortawesome/fontawesome-common-types/-/fontawesome-common-types-6.5.2.tgz",
      "integrity": "sha512-gBxPg3aVO6J0kpfHNILc+NMhXnqHumFxOmjYCFfOiLZfwhnnfhtsdA2hfJlDnj+8PjAs6kKQPenOTKj3Rf7zHw==",
      "hasInstallScript": true,
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/@fortawesome/fontawesome-svg-core": {
      "version": "6.5.2",
      "resolved": "https://registry.npmjs.org/@fortawesome/fontawesome-svg-core/-/fontawesome-svg-core-6.5.2.tgz",
      "integrity": "sha512-5CdaCBGl8Rh9ohNdxeeTMxIj8oc3KNBgIeLMvJosBMdslK/UnEB8rzyDRrbKdL1kDweqBPo4GT9wvnakHWucZw==",
      "hasInstallScript": true,
      "peer": true,
      "dependencies": {
        "@fortawesome/fontawesome-common-types": "6.5.2"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/@fortawesome/free-solid-svg-icons": {
      "version": "6.5.2",
      "resolved": "https://registry.npmjs.org/@fortawesome/free-solid-svg-icons/-/free-solid-svg-icons-6.5.2.tgz",
      "integrity": "sha512-QWFZYXFE7O1Gr1dTIp+D6UcFUF0qElOnZptpi7PBUMylJh+vFmIedVe1Ir6RM1t2tEQLLSV1k7bR4o92M+uqlw==",
      "hasInstallScript": true,
      "dependencies": {
        "@fortawesome/fontawesome-common-types": "6.5.2"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/@fortawesome/react-fontawesome": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/@fortawesome/react-fontawesome/-/react-fontawesome-0.2.0.tgz",
      "integrity": "sha512-uHg75Rb/XORTtVt7OS9WoK8uM276Ufi7gCzshVWkUJbHhh3svsUUeqXerrM96Wm7fRiDzfKRwSoahhMIkGAYHw==",
      "dependencies": {
        "prop-types": "^15.8.1"
      },
      "peerDependencies": {
        "@fortawesome/fontawesome-svg-core": "~1 || ~6",
        "react": ">=16.3"
      }
    },