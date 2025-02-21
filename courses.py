courses = {
    "University of South Florida": {
        "ACG": {
            "2021": {
                "Class Full Name": "Principles of Financial Accounting",
                "Description": "Study of basic accounting principles including the recording and reporting of financial activity. The preparation and interpretation of financial statements.",
                "CoReqs": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "2071": {
                "Class Full Name": "Principles of Managerial Accounting",
                "Description": "A study of the accountant\u2019s role in assisting management in the planning and controlling of business activities.",
                "CoReqs": "N/A",
                "Prereqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "2021",
                        "Grade": "C"
                    }
                ],
                "Credit Hours": 3
            },
            "3074": {
                "Class Full Name": "Managerial Accounting for Non-Business Majors",
                "Description": "The study of the uses of accounting data internally by managers in planning and controlling the affairs of organizations.",
                "Mingrade_coreq": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "3103": {
                "Class Full Name": "Intermediate Financial Accounting I",
                "Description": "Theory and methodology underlying financial reporting, including the FASB\u2019s conceptual framework, the accounting process, financial statements, accounting changes, present value applications, and current assets.",
                "CoReqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "3341",
                        "Grade": "C"
                    }
                ],
                "Mingrade_coreq": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "3113": {
                "Class Full Name": "Intermediate Financial Accounting II",
                "Description": "Continuation of ACG 3103. Topics covered include property, plant and equipment, intangibles, current liabilities, long-term debt, leases, tax allocation, statement of cash flows.",
                "CoReqs": "N/A",
                "Prereqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "3103",
                        "Grade": "C"
                    },
                    [
                        {
                            "Department": "ACG",
                            "Course Code": "3341",
                            "Grade": "C"
                        },
                        {
                            "Department": "ACG",
                            "Course Code": "3401",
                            "Grade": "C"
                        },
                        {
                            "Department": "TAX",
                            "Course Code": "4001",
                            "Grade": "C"
                        }
                    ]
                ],
                "Credit Hours": 3
            },
            "3341": {
                "Class Full Name": "Cost Accounting and Control I",
                "Description": "Deals with cost accounting systems for different entities, cost behavior patterns, cost-volume-profit analysis, relevant information for decision making, and budgets and standard costs for planning and control.",
                "Prereqs": {
                    "AND": [
                        {
                            "OR": [
                                {
                                    "Department": "ACG",
                                    "Course Code": "2021",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "ACG",
                                    "Course Code": "2021C",
                                    "Grade": "C"
                                },
                                {
                                    "AND": [
                                        {
                                            "Department": "ACG",
                                            "Course Code": "2001",
                                            "Grade": "C"
                                        },
                                        {
                                            "Department": "ACG",
                                            "Course Code": "2011",
                                            "Grade": "C"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "Department": "ACG",
                            "Course Code": "2071",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "ACG",
                            "Course Code": "3103",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            }
        },
        "EEL": {
            "4835": {
                "Class Full Name": "Programming Design",
                "Description": "This course provides essential knowledge for engineering students to design computer programs to solve various tasks in real-world applications.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "N/A"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3394": {
                "Class Full Name": "Programming with C",
                "Description": "An introductory course to provide the fundamentals of computer language for electrical engineering students. Skills on syntax, functions, data, input and output, algorithm, and creating solutions for engineering problems using C.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3115L": {
                "Class Full Name": "Laboratory I",
                "Description": "Basic circuit theory applications; computer-aided design tools, electrical measurement techniques.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3373",
                            "Grade": "N/A"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "3163C": {
                "Class Full Name": "Computer Tool Lab",
                "Description": "An introductory course to provide the knowledge on using Matlab and Simulink for solving wide range of problems in the field of electrical engineering - differential equation, convolution, Fourier Series and Transform, Laplace Transform, DSP, and etc.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4102",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 1
            },
            "3705": {
                "Class Full Name": "Fundamentals of Digital Circuits",
                "Description": "Binary number systems; truth functions; Boolean algebra; canonical forms; minimization of combinational logic circuits; synchronous and Asynchronous logic circuits. HDL\u00b4s introduction.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3705L": {
                "Class Full Name": "Fundamentals of Digital Circuits Laboratory",
                "Description": "Develop designs and demonstrate logic concepts. Schematic capture for design implementation, simulation and design verification.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3705",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "4102": {
                "Class Full Name": "Signals and Systems",
                "Description": "Provides further study in the analysis of signals and linear systems. Includes time and frequency domain points of view such as Laplace and Fourier analysis as well as convolution.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3420",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3163C",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            }
        },
        "EGN": {
            "3000": {
                "Class Full Name": "Foundations of Engineering",
                "Description": "Introduction to the USF College of Engineering disciplines and the engineering profession. Course will provide you with knowledge of resources to help you succeed. Course topics include academic policies and procedures, study skills, and career planning.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 0
            },
            "3000L": {
                "Class Full Name": "Foundations of Engineering Lab",
                "Description": "Introduction to Engineering and its disciplines incorporating examples of tools and techniques used in design and presentation. Laboratory exercises will include computer tools, engineering design, team projects, and oral and written communication skills.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3443": {
                "Class Full Name": "Probability and Statistics for Engineers",
                "Description": "An introduction to concepts of probability and statistical analysis with special emphasis on critical interpretation of data, comparing and contrasting claims, critical thinking, problem solving, and writing.",
                "Prereqs": {
                    "OR": [
                        {
                            "Department": "MAC",
                            "Course Code": "2282",
                            "Grade": "C"
                        },
                        {
                            "Department": "MAC",
                            "Course Code": "2312",
                            "Grade": "C"
                        },
                        {
                            "Department": "AP Calculus",
                            "Course Code": "BC",
                            "Grade": "4"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3615": {
                "Class Full Name": "Engineering Economics with Social and Global Implications",
                "Description": "Presents basic economic models used to evaluate engineering project investments with an understanding of the implications of human and cultural diversity on financial decisions through lectures, problem solving, and critical writing.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            }
        },
        "EEE": {
            "3394": {
                "Class Full Name": "Electrical Engineering Science I - Electronic Materials",
                "Description": "This course provides electrical and computer engineering students with a strong background in material science and quantum physics as they relate to electrical/electronic material and device properties and applications.",
                "Prereqs": {
                    "AND": [
                        {
                            "OR": [
                                {
                                    "Department": "CHS",
                                    "Course Code": "2440",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "CMH",
                                    "Course Code": "2045",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "AP",
                                    "Course Code": "Chemistry",
                                    "Grade": "4"
                                }
                            ]
                        },
                        {
                            "OR": [
                                {
                                    "Department": "PHY",
                                    "Course Code": "2048",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "PHY",
                                    "Course Code": "2060",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "AP",
                                    "Course Code": "Physics C: Electricity and Magnetism",
                                    "Grade": "4"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": {
                    "OR": [
                        {
                            "Department": "MAC",
                            "Course Code": "2283",
                            "Grade": "C"
                        },
                        {
                            "Department": "MAC",
                            "Course Code": "2313",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            }
        }
    },
    "Hillsborough CC": {
        "ENC": {
            "1101": {
                "Class Full Name": "English Composition I",
                "Description": "English Class",
                "CoReqs": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            }
        }
    }
}
