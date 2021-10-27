import math

pumps = {'cheap': {'efficiency': 0.80,
                   20: 200,
                   30: 220,
                   40: 242,
                   50: 266,
                   60: 293,
                   70: 322,
                   80: 354,
                   90: 390,
                   100: 429,
                   110: 472,
                   120: 519},
         'value': {'efficiency': 0.83,
                   20: 240,
                   30: 264,
                   40: 290,
                   50: 319,
                   60: 351,
                   70: 387,
                   80: 425,
                   90: 468,
                   100: 514,
                   110: 566,
                   120: 622},
         'standard': {'efficiency': 0.86,
                      20: 288,
                      30: 317,
                      40: 348,
                      50: 383,
                      60: 422,
                      70: 464,
                      80: 510,
                      90: 561,
                      100: 617,
                      110: 679,
                      120: 747},
         'high-grade': {'efficiency': 0.89,
                        20: 346,
                        30: 380,
                        40: 418,
                        50: 460,
                        60: 506,
                        70: 557,
                        80: 612,
                        90: 673,
                        100: 741,
                        110: 815,
                        120: 896},
         'premium': {'efficiency': 0.92,
                     20: 415,
                     30: 456,
                     40: 502,
                     50: 552,
                     60: 607,
                     70: 668,
                     80: 735,
                     90: 808,
                     100: 889,
                     110: 978,
                     120: 1076}}

