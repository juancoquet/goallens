from datetime import date

# test_create_upload_dict
EXPECTED_UPLOAD_DICT = {
            # premier league teams 2018-2019
            'b8fd03ef': {
                'id': 'b8fd03ef',
                'name': 'Manchester City',
                'short_name': 'Manchester City'
            },
            '822bd0ba': {
                'id': '822bd0ba',
                'name': 'Liverpool',
                'short_name': 'Liverpool'
            },
            'cff3d9bb': {
                'id': 'cff3d9bb',
                'name': 'Chelsea',
                'short_name': 'Chelsea'
            },
            '361ca564': {
                'id': '361ca564',
                'name': 'Tottenham Hotspur',
                'short_name': 'Tottenham'
            },
            '18bb7c10': {
                'id': '18bb7c10',
                'name': 'Arsenal',
                'short_name': 'Arsenal'
            },
            '19538871': {
                'id': '19538871',
                'name': 'Manchester United',
                'short_name': 'Manchester Utd'
            },
            '8cec06e1': {
                'id': '8cec06e1',
                'name': 'Wolverhampton Wanderers',
                'short_name': 'Wolves'
            },
            'd3fd31cc': {
                'id': 'd3fd31cc',
                'name': 'Everton',
                'short_name': 'Everton'
            },
            'a2d435b3': {
                'id': 'a2d435b3',
                'name': 'Leicester City',
                'short_name': 'Leicester City'
            },
            '7c21e445': {
                'id': '7c21e445',
                'name': 'West Ham United',
                'short_name': 'West Ham'
            },
            '2abfe087': {
                'id': '2abfe087',
                'name': 'Watford',
                'short_name': 'Watford'
            },
            '47c64c55': {
                'id': '47c64c55',
                'name': 'Crystal Palace',
                'short_name': 'Crystal Palace'
            },
            'b2b47a98': {
                'id': 'b2b47a98',
                'name': 'Newcastle United',
                'short_name': 'Newcastle Utd'
            },
            '4ba7cbea': {
                'id': '4ba7cbea',
                'name': 'Bournemouth',
                'short_name': 'Bournemouth'
            },
            '943e8050': {
                'id': '943e8050',
                'name': 'Burnley',
                'short_name': 'Burnley'
            },
            '33c895d4': {
                'id': '33c895d4',
                'name': 'Southampton',
                'short_name': 'Southampton'
            },
            'd07537b9': {
                'id': 'd07537b9',
                'name': 'Brighton & Hove Albion',
                'short_name': 'Brighton'
            },
            '75fae011': {
                'id': '75fae011',
                'name': 'Cardiff City',
                'short_name': 'Cardiff City'
            },
            'fd962109': {
                'id': 'fd962109',
                'name': 'Fulham',
                'short_name': 'Fulham'
            },
            'f5922ca5': {
                'id': 'f5922ca5',
                'name': 'Huddersfield Town',
                'short_name': 'Huddersfield'
            },
            # championship teams 2018-2019
            '1c781004': {
                'id': '1c781004',
                'name': 'Norwich City',
                'short_name': 'Norwich City'
            },
            '1df6b87e': {
                'id': '1df6b87e',
                'name': 'Sheffield United',
                'short_name': 'Sheffield Utd'
            },
            '5bfb9659': {
                'id': '5bfb9659',
                'name': 'Leeds United',
                'short_name': 'Leeds United'
            },
            '60c6b05f': {
                'id': '60c6b05f',
                'name': 'West Bromwich Albion',
                'short_name': 'West Brom'
            },
            '8602292d': {
                'id': '8602292d',
                'name': 'Aston Villa',
                'short_name': 'Aston Villa'
            },
            '26ab47ee': {
                'id': '26ab47ee',
                'name': 'Derby County',
                'short_name': 'Derby County'
            },
            '7f59c601': {
                'id': '7f59c601',
                'name': 'Middlesbrough',
                'short_name': 'Middlesbrough'
            },
            '93493607': {
                'id': '93493607',
                'name': 'Bristol City',
                'short_name': 'Bristol City'
            },
            'e4a775cb': {
                'id': 'e4a775cb',
                'name': 'Nottingham Forest',
                'short_name': 'Nott\'ham Forest'
            },
            'fb10988f': {
                'id': 'fb10988f',
                'name': 'Swansea City',
                'short_name': 'Swansea City'
            },
            'cd051869': {
                'id': 'cd051869',
                'name': 'Brentford',
                'short_name': 'Brentford'
            },
            'bba7d733': {
                'id': 'bba7d733',
                'name': 'Sheffield Wednesday',
                'short_name': 'Sheffield Weds'
            },
            'bd8769d1': {
                'id': 'bd8769d1',
                'name': 'Hull City',
                'short_name': 'Hull City'
            },
            '22df8478': {
                'id': '22df8478',
                'name': 'Preston North End',
                'short_name': 'Preston'
            },
            'e090f40b': {
                'id': 'e090f40b',
                'name': 'Blackburn Rovers',
                'short_name': 'Blackburn'
            },
            '17892952': {
                'id': '17892952',
                'name': 'Stoke City',
                'short_name': 'Stoke City'
            },
            'ec79b7c2': {
                'id': 'ec79b7c2',
                'name': 'Birmingham City',
                'short_name': 'Birmingham City'
            },
            'e59ddc76': {
                'id': 'e59ddc76',
                'name': 'Wigan Athletic',
                'short_name': 'Wigan Athletic'
            },
            'a757999c': {
                'id': 'a757999c',
                'name': 'Queens Park Rangers',
                'short_name': 'QPR'
            },
            'b0ac61ff': {
                'id': 'b0ac61ff',
                'name': 'Reading',
                'short_name': 'Reading'
            },
            'e3c537a1': {
                'id': 'e3c537a1',
                'name': 'Millwall',
                'short_name': 'Millwall'
            },
            '375d66f1': {
                'id': '375d66f1',
                'name': 'Rotherham United',
                'short_name': 'Rotherham Utd'
            },
            '445d3104': {
                'id': '445d3104',
                'name': 'Bolton Wanderers',
                'short_name': 'Bolton'
            },
            'b74092de': {
                'id': 'b74092de',
                'name': 'Ipswich Town',
                'short_name': 'Ipswich Town'
            },
            # premier league teams 2019-2020
            # (no new teams)
            # championship teams 2019-2020
            'e297cd13': {
                'id': 'e297cd13',
                'name': 'Luton Town',
                'short_name': 'Luton Town'
            },
            '293cb36b': {
                'id': '293cb36b',
                'name': 'Barnsley',
                'short_name': 'Barnsley'
            },
            '7a8db6d4': {
                'id': '7a8db6d4',
                'name': 'Charlton Athletic',
                'short_name': 'Charlton Ath'
            },            
        }

# test_get_fixture_ids
EXPECTED_FIXTURE_IDS = [
    '928467bd',
    '71c8a43e',
    '34b99058',
    '38111659',
    'a802f51e',
    'd402cacd',
    '404ee5d3',
    '1405a610',
    'bf4afd61',
    'd0583d0d',
    'ff7eda21',
    '3ea63f4b',
    '7ad0ed82',
    '894d0ca5',
    'b2a48847',
    'f35c8c3a',
    'a4ba771e',
    '7ca12d31',
    'aebf58b9',
    'd8a7f871',
    '3e805eff',
    '4f4fd2d8',
    '48fcf75b',
    '7c1c4078',
    '89fbf2a3',
    'baece203',
    '102b241e',
    '7728bd7e',
    '16119ef2',
    'c224d1e8',
    'bfd4d929',
    '164148a8',
    '230f4fac',
    '3d899563',
    '495db223',
    '533c240c',
    '5b9865ad',
    'af072d61',
    '70303b7b',
    '0b6b8aaf',
    'cde24fee',
    '0fa0a658',
    '1d3bbc27',
    '1d812c17',
    '6d0266a1',
    'e5f9905d',
    '1c7bccd4',
    '886c59ae',
    '8257eda8',
    'b26df467',
    'ebbb65f5',
    'e30adc4b',
    '4672d0d7',
    '707ee0eb',
    'f97b0ce8',
    '966fb8b0',
    'd76eb681',
    'fe3e2bec',
    '02e3ae79',
    'd5fa0563',
    '1224c8ae',
    '1d4b5564',
    '23ec5db0',
    '37a51188',
    '3b180c0d',
    '4c088365',
    '704e536e',
    '1b9f4fc3',
    '40d77688',
    'ce7501cd',
    'aafb2d3a',
    '2b83068d',
    '2f9439d0',
    'aaed1c4e',
    'e50b8e5b',
    '23fe51bc',
    '0481092b',
    '078b24d4',
    '9575566f',
    'e4a80056',
    '0fa45675',
    '34685c72',
    '3529c097',
    '4df24be7',
    '644a3723',
    'c17538b0',
    'd71c01eb',
    'f334b1dc',
    '95c3f0c8',
    'f63044fd',
    '3e9712d7',
    'e0a4db2d',
    '1ef8e186',
    '43aa7711',
    'f728ceea',
    '082dc9ef',
    'efe2b576',
    '077b30ff',
    '16f28685',
    'a31a1d67',
    '9e35d172',
    '21606115',
    '21f39009',
    '2206646c',
    'a3427b2c',
    'ac4523c2',
    'afbdd3aa',
    '0b8b7f66',
    '25d28387',
    'efe9c8f4',
    'e92f4d2c',
    '99680077',
    '553c5b11',
    '559f666e',
    '698f846d',
    'ec70bb2c',
    '8e13e609',
    '014bbabe',
    '2794f89d',
    '47880eb7',
    'a7dc884b',
    '0b1da656',
    '19a8b14e',
    '219643bc',
    '464461f5',
    'd0f6bac9',
    'd4aea4c0',
    'd16305c7',
    'a1d9d65f',
    'f6f8808e',
    'f43fa290',
    '1722ba52',
    '2c240ae6',
    '86428aca',
    'aa1ff9cd',
    '3f1fdbad',
    '39fce32e',
    '53a77072',
    'aa2284c2',
    'e88d9028',
    'fd541a1f',
    '4d718594',
    '292d0f46',
    '367829b6',
    '3f316110',
    '614c7c1f',
    '8b04b0d5',
    'de0ec650',
    '8a9fa2d9',
    '372828cb',
    '1b69dd66',
    '56da163b',
    '90976b40',
    'b7f0ca17',
    'bf9c0d50',
    '529b20fa',
    '559e812a',
    '5d9f7fe3',
    'daad5806',
    'a48c4638',
    'f33bb4b3',
    '3b2eb152',
    '4c3c57fa',
    'b1b5e590',
    'b75094e0',
    'a47901a8',
    '240ac5ad',
    'e9e002fb',
    'bed05936',
    '1163ec4a',
    'b9d1d1a7',
    '223124ce',
    '473db5a3',
    '5e599d06',
    'd50390a8',
    'e8b74ca0',
    '733c0243',
    'a58df282',
    'a1a20337',
    'eebe09b9',
    '010301bf',
    '048fa915',
    '5b1ecf02',
    '960ce979',
    'b23c6c90',
    'd9a73d72',
    'b3d5292f',
    '4b8063da',
    '6defd3a2',
    'd7b72d7f',
    '36dc1eb8',
    '6edbd555',
    'a8ab1213',
    '1f2bd890',
    'a6e8ab71',
    'f66bbb03',
    '850e18c6',
    '9892a4f1',
    'aaada016',
    '9b72407a',
    'ac409026',
    'a7902bb1',
    'ce2fad1e',
    'dc2a86e8',
    '5bbec2c4',
    '9ae01aab',
    'ed58271e',
    'f6b7d570',
    '7fe3382b',
    'c5f47ccb',
    'e1fdc1f9',
    '17a5a8ef',
    '61cc2ca5',
    'bf752bf7',
    'd5b1eda9',
    'db192bf5',
    '39432697',
    '76ce7bd8',
    'ffb4946c',
    '46697bf6',
    '0333a4b6',
    '2550abdc',
    '4572cd0e',
    '9d6674f8',
    'bd044bad',
    'd4898eac',
    'e5a20f1e',
    'bd102a2b',
    'd2a888b6',
    '003ce1e3',
    '33b8c50a',
    '3deb145e',
    'ae7cb0c2',
    'ba03a070',
    '38d058ad',
    '354b03ac',
    'b36a7b4d',
    '709e2aa4',
    'efd768f0',
    '7b057bc1',
    '270dc7ba',
    '14d877cc',
    '476d12a9',
    '6b34e6af',
    'ab9e9e23',
    'db21a88a',
    'eef415ec',
    '88328013',
    'a6b40849',
    'e98d8736',
    '4e620966',
    '111b8b45',
    '9dbc60d4',
    'a11273b7',
    '738ade70',
    '9c238122',
    'ebfe971d',
    '6ce374b0',
    '2619bcb9',
    'bc091e86',
    'fdd364a6',
    '5947b8fb',
    '66823ac4',
    'bcdc3fb0',
    'c24b02bd',
    '4f00e03a',
    '09ec6552',
    '835d0c36',
    '485003ed',
    '3aee1ba7',
    '8edf3e12',
    'aeb979e2',
    '2cb790f2',
    '57d79762',
    '5d623dc0',
    '4df69c15',
    '2475762d',
    'ea2c2272',
    'a24ed8fc',
    '6a08610e',
    '7535d777',
    '947a04e9',
    'bf382825',
    'fcdf913d',
    '1b4c17ec',
    'c062bff0',
    '04416d35',
    '76f492dc',
    '18961bf7',
    '5825b217',
    'd659cbdf',
    '973a441a',
    'e5f403c2',
    '1abcdcde',
    '6ddd148a',
    'c4d88352',
    '4e501da1',
    '827d4651',
    '603174fb',
    'b1d3ebde',
    '481a9a3a',
    '8fc12d99',
    '49724d90',
    '4f61e5af',
    '54cdce8b',
    '66027e20',
    'c486cf76',
    '38757aa1',
    '965fbb94',
    'bc237647',
    'b4483d72',
    '37720dc3',
    'd7661a5f',
    'be321c59',
    '92aaad57',
    'c2c7ebbf',
    'cb52b4c8',
    '5df18070',
    '70507f3c',
    '5dffd237',
    'aa3a3540',
    '88e800c1',
    '8bed0062',
    'df13ee5b',
    'ee7944f1',
    'c2378113',
    '3d549d43',
    'c2481cad',
    '260c5c31',
    'ba9fd89a',
    '61407f3d',
    '7e51a0cb',
    'a26b0a22',
    '426dcb15',
    '5c57bea6',
    'f898c8ea',
    '3296482a',
    '1357ee3b',
    '1d9de580',
    '61422f26',
    '1f633005',
    'ae59ff28',
    '267d7e78',
    '3f83499d',
    'a24d3d6b',
    '476e8583',
    'b30bf2e8',
    '6630c721',
    'd2adf574',
    '668c9423',
    '88d08b7b',
    '21cbea56',
    'a7c5d31f',
    'eff6988f',
    '12f95828',
    '0903cee0',
    'f855bc55',
    '69a16f9d',
    '793f900e',
    '249bbdaa',
    '9594e0b4',
    'bbd4160f',
    'd4ce66f6',
    '9defdd38',
    'd2e788d0',
    '70598e52',
    '9979847f',
    'ca0b21bc',
    'bf25e016',
    'a80ba6fe',
    '2a3b8f05',
    '3873cc78',
    '3e5b45b7',
    '5ecaeb4b',
    '61616d45',
    '9099d1e5',
    '9cca4ba0',
    'a3f59c8e',
    'b6b1209d',
    'd4360fcd',
]

# test_get_fixture_dates
EXPECTED_FIXTURE_DATES = {
    '928467bd': date(2019, 8, 9),
    '71c8a43e': date(2019, 8, 10),
    '34b99058': date(2019, 8, 10),
    '38111659': date(2019, 8, 10),
    'a802f51e': date(2019, 8, 10),
    'd402cacd': date(2019, 8, 10),
    '404ee5d3': date(2019, 8, 10),
    '1405a610': date(2019, 8, 11),
    'bf4afd61': date(2019, 8, 11),
    'd0583d0d': date(2019, 8, 11),
    'ff7eda21': date(2019, 8, 17),
    '3ea63f4b': date(2019, 8, 17),
    '7ad0ed82': date(2019, 8, 17),
    '894d0ca5': date(2019, 8, 17),
    'b2a48847': date(2019, 8, 17),
    'f35c8c3a': date(2019, 8, 17),
    'a4ba771e': date(2019, 8, 17),
    '7ca12d31': date(2019, 8, 18),
    'aebf58b9': date(2019, 8, 18),
    'd8a7f871': date(2019, 8, 19),
    '3e805eff': date(2019, 8, 23),
    '4f4fd2d8': date(2019, 8, 24),
    '48fcf75b': date(2019, 8, 24),
    '7c1c4078': date(2019, 8, 24),
    '89fbf2a3': date(2019, 8, 24),
    'baece203': date(2019, 8, 24),
    '102b241e': date(2019, 8, 24),
    '7728bd7e': date(2019, 8, 25),
    '16119ef2': date(2019, 8, 25),
    'c224d1e8': date(2019, 8, 25),
    'bfd4d929': date(2019, 8, 31),
    '164148a8': date(2019, 8, 31),
    '230f4fac': date(2019, 8, 31),
    '3d899563': date(2019, 8, 31),
    '495db223': date(2019, 8, 31),
    '533c240c': date(2019, 8, 31),
    '5b9865ad': date(2019, 8, 31),
    'af072d61': date(2019, 8, 31),
    '70303b7b': date(2019, 9, 1),
    '0b6b8aaf': date(2019, 9, 1),
    'cde24fee': date(2019, 9, 14),
    '0fa0a658': date(2019, 9, 14),
    '1d3bbc27': date(2019, 9, 14),
    '1d812c17': date(2019, 9, 14),
    '6d0266a1': date(2019, 9, 14),
    'e5f9905d': date(2019, 9, 14),
    '1c7bccd4': date(2019, 9, 14),
    '886c59ae': date(2019, 9, 15),
    '8257eda8': date(2019, 9, 15),
    'b26df467': date(2019, 9, 16),
    'ebbb65f5': date(2019, 9, 20),
    'e30adc4b': date(2019, 9, 21),
    '4672d0d7': date(2019, 9, 21),
    '707ee0eb': date(2019, 9, 21),
    'f97b0ce8': date(2019, 9, 21),
    '966fb8b0': date(2019, 9, 21),
    'd76eb681': date(2019, 9, 22),
    'fe3e2bec': date(2019, 9, 22),
    '02e3ae79': date(2019, 9, 22),
    'd5fa0563': date(2019, 9, 22),
    '1224c8ae': date(2019, 9, 28),
    '1d4b5564': date(2019, 9, 28),
    '23ec5db0': date(2019, 9, 28),
    '37a51188': date(2019, 9, 28),
    '3b180c0d': date(2019, 9, 28),
    '4c088365': date(2019, 9, 28),
    '704e536e': date(2019, 9, 28),
    '1b9f4fc3': date(2019, 9, 28),
    '40d77688': date(2019, 9, 29),
    'ce7501cd': date(2019, 9, 30),
    'aafb2d3a': date(2019, 10, 5),
    '2b83068d': date(2019, 10, 5),
    '2f9439d0': date(2019, 10, 5),
    'aaed1c4e': date(2019, 10, 5),
    'e50b8e5b': date(2019, 10, 5),
    '23fe51bc': date(2019, 10, 5),
    '0481092b': date(2019, 10, 6),
    '078b24d4': date(2019, 10, 6),
    '9575566f': date(2019, 10, 6),
    'e4a80056': date(2019, 10, 6),
    '0fa45675': date(2019, 10, 19),
    '34685c72': date(2019, 10, 19),
    '3529c097': date(2019, 10, 19),
    '4df24be7': date(2019, 10, 19),
    '644a3723': date(2019, 10, 19),
    'c17538b0': date(2019, 10, 19),
    'd71c01eb': date(2019, 10, 19),
    'f334b1dc': date(2019, 10, 19),
    '95c3f0c8': date(2019, 10, 20),
    'f63044fd': date(2019, 10, 21),
    '3e9712d7': date(2019, 10, 25),
    'e0a4db2d': date(2019, 10, 26),
    '1ef8e186': date(2019, 10, 26),
    '43aa7711': date(2019, 10, 26),
    'f728ceea': date(2019, 10, 26),
    '082dc9ef': date(2019, 10, 26),
    'efe2b576': date(2019, 10, 27),
    '077b30ff': date(2019, 10, 27),
    '16f28685': date(2019, 10, 27),
    'a31a1d67': date(2019, 10, 27),
    '9e35d172': date(2019, 11, 2),
    '21606115': date(2019, 11, 2),
    '21f39009': date(2019, 11, 2),
    '2206646c': date(2019, 11, 2),
    'a3427b2c': date(2019, 11, 2),
    'ac4523c2': date(2019, 11, 2),
    'afbdd3aa': date(2019, 11, 2),
    '0b8b7f66': date(2019, 11, 2),
    '25d28387': date(2019, 11, 3),
    'efe9c8f4': date(2019, 11, 3),
    'e92f4d2c': date(2019, 11, 8),
    '99680077': date(2019, 11, 9),
    '553c5b11': date(2019, 11, 9),
    '559f666e': date(2019, 11, 9),
    '698f846d': date(2019, 11, 9),
    'ec70bb2c': date(2019, 11, 9),
    '8e13e609': date(2019, 11, 9),
    '014bbabe': date(2019, 11, 10),
    '2794f89d': date(2019, 11, 10),
    '47880eb7': date(2019, 11, 10),
    'a7dc884b': date(2019, 11, 23),
    '0b1da656': date(2019, 11, 23),
    '19a8b14e': date(2019, 11, 23),
    '219643bc': date(2019, 11, 23),
    '464461f5': date(2019, 11, 23),
    'd0f6bac9': date(2019, 11, 23),
    'd4aea4c0': date(2019, 11, 23),
    'd16305c7': date(2019, 11, 23),
    'a1d9d65f': date(2019, 11, 24),
    'f6f8808e': date(2019, 11, 25),
    'f43fa290': date(2019, 11, 30),
    '1722ba52': date(2019, 11, 30),
    '2c240ae6': date(2019, 11, 30),
    '86428aca': date(2019, 11, 30),
    'aa1ff9cd': date(2019, 11, 30),
    '3f1fdbad': date(2019, 11, 30),
    '39fce32e': date(2019, 12, 1),
    '53a77072': date(2019, 12, 1),
    'aa2284c2': date(2019, 12, 1),
    'e88d9028': date(2019, 12, 1),
    'fd541a1f': date(2019, 12, 3),
    '4d718594': date(2019, 12, 3),
    '292d0f46': date(2019, 12, 4),
    '367829b6': date(2019, 12, 4),
    '3f316110': date(2019, 12, 4),
    '614c7c1f': date(2019, 12, 4),
    '8b04b0d5': date(2019, 12, 4),
    'de0ec650': date(2019, 12, 4),
    '8a9fa2d9': date(2019, 12, 5),
    '372828cb': date(2019, 12, 5),
    '1b69dd66': date(2019, 12, 7),
    '56da163b': date(2019, 12, 7),
    '90976b40': date(2019, 12, 7),
    'b7f0ca17': date(2019, 12, 7),
    'bf9c0d50': date(2019, 12, 7),
    '529b20fa': date(2019, 12, 8),
    '559e812a': date(2019, 12, 8),
    '5d9f7fe3': date(2019, 12, 8),
    'daad5806': date(2019, 12, 8),
    'a48c4638': date(2019, 12, 9),
    'f33bb4b3': date(2019, 12, 14),
    '3b2eb152': date(2019, 12, 14),
    '4c3c57fa': date(2019, 12, 14),
    'b1b5e590': date(2019, 12, 14),
    'b75094e0': date(2019, 12, 14),
    'a47901a8': date(2019, 12, 14),
    '240ac5ad': date(2019, 12, 15),
    'e9e002fb': date(2019, 12, 15),
    'bed05936': date(2019, 12, 15),
    '1163ec4a': date(2019, 12, 16),
    'b9d1d1a7': date(2019, 12, 21),
    '223124ce': date(2019, 12, 21),
    '473db5a3': date(2019, 12, 21),
    '5e599d06': date(2019, 12, 21),
    'd50390a8': date(2019, 12, 21),
    'e8b74ca0': date(2019, 12, 21),
    '733c0243': date(2019, 12, 21),
    'a58df282': date(2019, 12, 22),
    'a1a20337': date(2019, 12, 22),
    'eebe09b9': date(2019, 12, 26),
    '010301bf': date(2019, 12, 26),
    '048fa915': date(2019, 12, 26),
    '5b1ecf02': date(2019, 12, 26),
    '960ce979': date(2019, 12, 26),
    'b23c6c90': date(2019, 12, 26),
    'd9a73d72': date(2019, 12, 26),
    'b3d5292f': date(2019, 12, 26),
    '4b8063da': date(2019, 12, 26),
    '6defd3a2': date(2019, 12, 27),
    'd7b72d7f': date(2019, 12, 28),
    '36dc1eb8': date(2019, 12, 28),
    '6edbd555': date(2019, 12, 28),
    'a8ab1213': date(2019, 12, 28),
    '1f2bd890': date(2019, 12, 28),
    'a6e8ab71': date(2019, 12, 28),
    'f66bbb03': date(2019, 12, 28),
    '850e18c6': date(2019, 12, 29),
    '9892a4f1': date(2019, 12, 29),
    'aaada016': date(2019, 12, 29),
    '9b72407a': date(2020, 1, 1),
    'ac409026': date(2020, 1, 1),
    'a7902bb1': date(2020, 1, 1),
    'ce2fad1e': date(2020, 1, 1),
    'dc2a86e8': date(2020, 1, 1),
    '5bbec2c4': date(2020, 1, 1),
    '9ae01aab': date(2020, 1, 1),
    'ed58271e': date(2020, 1, 1),
    'f6b7d570': date(2020, 1, 1),
    '7fe3382b': date(2020, 1, 2),
    'c5f47ccb': date(2020, 1, 10),
    'e1fdc1f9': date(2020, 1, 11),
    '17a5a8ef': date(2020, 1, 11),
    '61cc2ca5': date(2020, 1, 11),
    'bf752bf7': date(2020, 1, 11),
    'd5b1eda9': date(2020, 1, 11),
    'db192bf5': date(2020, 1, 11),
    '39432697': date(2020, 1, 11),
    '76ce7bd8': date(2020, 1, 12),
    'ffb4946c': date(2020, 1, 12),
    '46697bf6': date(2020, 1, 18),
    '0333a4b6': date(2020, 1, 18),
    '2550abdc': date(2020, 1, 18),
    '4572cd0e': date(2020, 1, 18),
    '9d6674f8': date(2020, 1, 18),
    'bd044bad': date(2020, 1, 18),
    'd4898eac': date(2020, 1, 18),
    'e5a20f1e': date(2020, 1, 18),
    'bd102a2b': date(2020, 1, 19),
    'd2a888b6': date(2020, 1, 19),
    '003ce1e3': date(2020, 1, 21),
    '33b8c50a': date(2020, 1, 21),
    '3deb145e': date(2020, 1, 21),
    'ae7cb0c2': date(2020, 1, 21),
    'ba03a070': date(2020, 1, 21),
    '38d058ad': date(2020, 1, 21),
    '354b03ac': date(2020, 1, 22),
    'b36a7b4d': date(2020, 1, 22),
    '709e2aa4': date(2020, 1, 22),
    'efd768f0': date(2020, 1, 23),
    '7b057bc1': date(2020, 1, 29),
    '270dc7ba': date(2020, 2, 1),
    '14d877cc': date(2020, 2, 1),
    '476d12a9': date(2020, 2, 1),
    '6b34e6af': date(2020, 2, 1),
    'ab9e9e23': date(2020, 2, 1),
    'db21a88a': date(2020, 2, 1),
    'eef415ec': date(2020, 2, 1),
    '88328013': date(2020, 2, 1),
    'a6b40849': date(2020, 2, 2),
    'e98d8736': date(2020, 2, 2),
    '4e620966': date(2020, 2, 8),
    '111b8b45': date(2020, 2, 8),
    '9dbc60d4': date(2020, 2, 9),
    'a11273b7': date(2020, 2, 14),
    '738ade70': date(2020, 2, 15),
    '9c238122': date(2020, 2, 15),
    'ebfe971d': date(2020, 2, 16),
    '6ce374b0': date(2020, 2, 16),
    '2619bcb9': date(2020, 2, 17),
    'bc091e86': date(2020, 2, 19),
    'fdd364a6': date(2020, 2, 22),
    '5947b8fb': date(2020, 2, 22),
    '66823ac4': date(2020, 2, 22),
    'bcdc3fb0': date(2020, 2, 22),
    'c24b02bd': date(2020, 2, 22),
    '4f00e03a': date(2020, 2, 22),
    '09ec6552': date(2020, 2, 23),
    '835d0c36': date(2020, 2, 23),
    '485003ed': date(2020, 2, 23),
    '3aee1ba7': date(2020, 2, 24),
    '8edf3e12': date(2020, 2, 28),
    'aeb979e2': date(2020, 2, 29),
    '2cb790f2': date(2020, 2, 29),
    '57d79762': date(2020, 2, 29),
    '5d623dc0': date(2020, 2, 29),
    '4df69c15': date(2020, 2, 29),
    '2475762d': date(2020, 3, 1),
    'ea2c2272': date(2020, 3, 1),
    'a24ed8fc': date(2020, 3, 7),
    '6a08610e': date(2020, 3, 7),
    '7535d777': date(2020, 3, 7),
    '947a04e9': date(2020, 3, 7),
    'bf382825': date(2020, 3, 7),
    'fcdf913d': date(2020, 3, 7),
    '1b4c17ec': date(2020, 3, 7),
    'c062bff0': date(2020, 3, 8),
    '04416d35': date(2020, 3, 8),
    '76f492dc': date(2020, 3, 9),
    '18961bf7': date(2020, 6, 17),
    '5825b217': date(2020, 6, 17),
    'd659cbdf': date(2020, 6, 19),
    '973a441a': date(2020, 6, 19),
    'e5f403c2': date(2020, 6, 20),
    '1abcdcde': date(2020, 6, 20),
    '6ddd148a': date(2020, 6, 20),
    'c4d88352': date(2020, 6, 20),
    '4e501da1': date(2020, 6, 21),
    '827d4651': date(2020, 6, 21),
    '603174fb': date(2020, 6, 21),
    'b1d3ebde': date(2020, 6, 22),
    '481a9a3a': date(2020, 6, 23),
    '8fc12d99': date(2020, 6, 23),
    '49724d90': date(2020, 6, 24),
    '4f61e5af': date(2020, 6, 24),
    '54cdce8b': date(2020, 6, 24),
    '66027e20': date(2020, 6, 24),
    'c486cf76': date(2020, 6, 24),
    '38757aa1': date(2020, 6, 25),
    '965fbb94': date(2020, 6, 25),
    'bc237647': date(2020, 6, 25),
    'b4483d72': date(2020, 6, 27),
    '37720dc3': date(2020, 6, 28),
    'd7661a5f': date(2020, 6, 29),
    'be321c59': date(2020, 6, 30),
    '92aaad57': date(2020, 7, 1),
    'c2c7ebbf': date(2020, 7, 1),
    'cb52b4c8': date(2020, 7, 1),
    '5df18070': date(2020, 7, 1),
    '70507f3c': date(2020, 7, 2),
    '5dffd237': date(2020, 7, 2),
    'aa3a3540': date(2020, 7, 4),
    '88e800c1': date(2020, 7, 4),
    '8bed0062': date(2020, 7, 4),
    'df13ee5b': date(2020, 7, 4),
    'ee7944f1': date(2020, 7, 4),
    'c2378113': date(2020, 7, 5),
    '3d549d43': date(2020, 7, 5),
    'c2481cad': date(2020, 7, 5),
    '260c5c31': date(2020, 7, 5),
    'ba9fd89a': date(2020, 7, 6),
    '61407f3d': date(2020, 7, 7),
    '7e51a0cb': date(2020, 7, 7),
    'a26b0a22': date(2020, 7, 7),
    '426dcb15': date(2020, 7, 8),
    '5c57bea6': date(2020, 7, 8),
    'f898c8ea': date(2020, 7, 8),
    '3296482a': date(2020, 7, 8),
    '1357ee3b': date(2020, 7, 9),
    '1d9de580': date(2020, 7, 9),
    '61422f26': date(2020, 7, 9),
    '1f633005': date(2020, 7, 11),
    'ae59ff28': date(2020, 7, 11),
    '267d7e78': date(2020, 7, 11),
    '3f83499d': date(2020, 7, 11),
    'a24d3d6b': date(2020, 7, 11),
    '476e8583': date(2020, 7, 12),
    'b30bf2e8': date(2020, 7, 12),
    '6630c721': date(2020, 7, 12),
    'd2adf574': date(2020, 7, 12),
    '668c9423': date(2020, 7, 13),
    '88d08b7b': date(2020, 7, 14),
    '21cbea56': date(2020, 7, 15),
    'a7c5d31f': date(2020, 7, 15),
    'eff6988f': date(2020, 7, 15),
    '12f95828': date(2020, 7, 15),
    '0903cee0': date(2020, 7, 16),
    'f855bc55': date(2020, 7, 16),
    '69a16f9d': date(2020, 7, 16),
    '793f900e': date(2020, 7, 16),
    '249bbdaa': date(2020, 7, 17),
    '9594e0b4': date(2020, 7, 18),
    'bbd4160f': date(2020, 7, 19),
    'd4ce66f6': date(2020, 7, 19),
    '9defdd38': date(2020, 7, 20),
    'd2e788d0': date(2020, 7, 20),
    '70598e52': date(2020, 7, 20),
    '9979847f': date(2020, 7, 21),
    'ca0b21bc': date(2020, 7, 21),
    'bf25e016': date(2020, 7, 22),
    'a80ba6fe': date(2020, 7, 22),
    '2a3b8f05': date(2020, 7, 26),
    '3873cc78': date(2020, 7, 26),
    '3e5b45b7': date(2020, 7, 26),
    '5ecaeb4b': date(2020, 7, 26),
    '61616d45': date(2020, 7, 26),
    '9099d1e5': date(2020, 7, 26),
    '9cca4ba0': date(2020, 7, 26),
    'a3f59c8e': date(2020, 7, 26),
    'b6b1209d': date(2020, 7, 26),
    'd4360fcd': date(2020, 7, 26),
}
