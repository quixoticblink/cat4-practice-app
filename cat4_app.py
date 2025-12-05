import streamlit as st
import time

# --- 1. QUIZ DATA SETUP ---
# We store the questions, options, and answers for 10 papers here.

PAPERS = {
    "Paper 1": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Granite | Marble | Slate",
            "options": ["Rock", "Limestone", "Hard", "Build", "Stone"],
            "answer": "Limestone",
            "explanation": "Granite, Marble, and Slate are specific types of rock. Limestone is also a specific type."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Cautious : Careless :: Private : ______",
            "options": ["General", "Public", "Secret", "Hidden", "Quiet"],
            "answer": "Public",
            "explanation": "Cautious is the opposite (antonym) of Careless. Private is the opposite of Public."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Geometry | Algebra | Calculus",
            "options": ["School", "Science", "Trigonometry", "Equations", "Difficult"],
            "answer": "Trigonometry",
            "explanation": "The first three are specific branches of mathematics. Trigonometry is also a specific branch."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[12 -> 4] and [27 -> 9]. Apply the same rule to [18 -> ?]",
            "options": ["3", "5", "6", "8", "2"],
            "answer": "6",
            "explanation": "The rule is divide by 3. 18 / 3 = 6."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 5, 11, 23, 47, ___",
            "options": ["94", "95", "80", "53", "105"],
            "answer": "95",
            "explanation": "The rule is (x2) + 1. 47 * 2 + 1 = 95."
        },
        {
            "category": "Number Analogies",
            "question": "[5 -> 24] and [7 -> 48]. Apply the same rule to [9 -> ?]",
            "options": ["80", "81", "79", "63", "90"],
            "answer": "80",
            "explanation": "The rule is Square the number, then subtract 1 (n^2 - 1). 9*9 = 81 - 1 = 80."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Square w/ horizontal line. Shape 2: Circle w/ horizontal line. Shape 3: Triangle w/ horizontal line. Which shape belongs?",
            "options": ["Square w/ vertical line", "Hexagon w/ diagonal line", "Pentagon w/ horizontal line", "Circle w/ cross"],
            "answer": "Pentagon w/ horizontal line",
            "explanation": "The rule is: Any shape with a single horizontal line splitting it."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Arrow Up] -> [Arrow Down]. Row 2: [Triangle Left] -> [?]",
            "options": ["Triangle Left", "Triangle Right", "Triangle Up", "Triangle Down"],
            "answer": "Triangle Right",
            "explanation": "The rule is rotate 180 degrees or reverse direction."
        },
        {
            "category": "Figure Analysis (Paper Folding)",
            "question": "Fold a square diagonally (bottom-left to top-right). Punch hole in center of folded triangle. Unfolded view?",
            "options": ["One hole center", "Two holes (Bottom-Left, Top-Right)", "Two holes (Top-Left, Bottom-Right)", "Four holes"],
            "answer": "Two holes (Top-Left, Bottom-Right)",
            "explanation": "Symmetry across the diagonal fold creates holes on the off-axis corners."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Perfect Circle. Where is it hidden?",
            "options": ["Brick wall drawing", "Overlapping triangles", "Bicycle drawing", "Checkerboard"],
            "answer": "Bicycle drawing",
            "explanation": "Only the bicycle contains curved lines/circles."
        }
    ],
    "Paper 2": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Sofa | Stool | Armchair",
            "options": ["Cushion", "Seat", "Bench", "Wood", "Relax"],
            "answer": "Bench",
            "explanation": "Sofa, Stool, and Armchair are types of furniture you sit on. Bench is also furniture you sit on."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Expand : Contract :: Ascend : ______",
            "options": ["Rise", "Descend", "Height", "Mountain", "Climb"],
            "answer": "Descend",
            "explanation": "Expand/Contract are antonyms. Ascend/Descend are antonyms."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Jupiter | Mars | Venus",
            "options": ["Star", "Space", "Saturn", "Galaxy", "Moon"],
            "answer": "Saturn",
            "explanation": "These are specific planets in our solar system."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[6 -> 11] and [8 -> 15]. Apply rule to [10 -> ?]",
            "options": ["18", "21", "19", "20", "22"],
            "answer": "19",
            "explanation": "Rule: (x2) - 1. 10 * 2 = 20 - 1 = 19."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 81, 64, 49, 36, ___",
            "options": ["24", "30", "25", "27", "16"],
            "answer": "25",
            "explanation": "Descending squares: 9^2, 8^2, 7^2, 6^2. Next is 5^2 (25)."
        },
        {
            "category": "Number Analogies",
            "question": "[4 -> 20] and [5 -> 30]. Apply rule to [9 -> ?]",
            "options": ["90", "72", "45", "81", "100"],
            "answer": "90",
            "explanation": "Rule: Multiply by the next integer (n * (n+1)). 9 * 10 = 90."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Shield Down. Shape 2: Heart Down. Shape 3: Arrow Down. Which belongs?",
            "options": ["Triangle Up", "Diamond", "Pentagon Down", "Circle"],
            "answer": "Pentagon Down",
            "explanation": "All shapes must be pointing downwards."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [1 Black Circle] -> [3 White Circles]. Row 2: [1 Black Square] -> [?]",
            "options": ["3 Black Squares", "1 White Square", "3 White Squares", "2 White Squares"],
            "answer": "3 White Squares",
            "explanation": "Rule: Triple the shape count and invert color (Black to White)."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Left-to-Right. Punch hole Top-Left of folded shape. Unfold?",
            "options": ["Two holes near Top-Center", "Top-Left and Bottom-Left", "Center", "Top-Right and Bottom-Right"],
            "answer": "Two holes near Top-Center",
            "explanation": "Punching the top-left of the folded strip (which is the crease) creates a mirrored pair at the top center."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Equilateral Triangle. Where is it hidden?",
            "options": ["Square Window", "5-Pointed Star", "Staircase", "Crescent Moon"],
            "answer": "5-Pointed Star",
            "explanation": "The points of a standard star are small equilateral triangles."
        }
    ],
    "Paper 3": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Apple | Pear | Banana",
            "options": ["Carrot", "Tomato", "Orange", "Potato", "Lettuce"],
            "answer": "Orange",
            "explanation": "Apple, Pear, and Banana are all fruits. Orange is also a fruit. The others are vegetables."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Day : Night :: Summer : ______",
            "options": ["Spring", "Autumn", "Winter", "Sun", "Cold"],
            "answer": "Winter",
            "explanation": "Day is the opposite of Night. Summer is the opposite season to Winter."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Football | Rugby | Hockey",
            "options": ["Swimming", "Running", "Tennis", "Cycling", "Gymnastics"],
            "answer": "Tennis",
            "explanation": "These are all sports played with a ball or object (puck/ball) and involve teams/matches. Tennis fits best."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[3 -> 12] and [5 -> 20]. Apply the same rule to [7 -> ?]",
            "options": ["21", "28", "30", "35", "14"],
            "answer": "28",
            "explanation": "Rule: Multiply by 4. 7 * 4 = 28."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 2, 4, 8, 16, ___",
            "options": ["24", "32", "30", "20", "48"],
            "answer": "32",
            "explanation": "Doubling pattern: x2. 16 * 2 = 32."
        },
        {
            "category": "Number Analogies",
            "question": "[10 -> 5] and [20 -> 10]. Apply the same rule to [50 -> ?]",
            "options": ["25", "100", "40", "30", "15"],
            "answer": "25",
            "explanation": "Rule: Divide by 2. 50 / 2 = 25."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Triangle. Shape 2: Square. Shape 3: Pentagon. Which belongs?",
            "options": ["Circle", "Hexagon", "Crescent", "Line"],
            "answer": "Hexagon",
            "explanation": "All are regular polygons with increasing sides (3, 4, 5). Hexagon (6) fits the category of polygons."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Circle] -> [Circle + Dot]. Row 2: [Square] -> [?]",
            "options": ["Square", "Square + Dot", "Circle + Dot", "Triangle"],
            "answer": "Square + Dot",
            "explanation": "Rule: Add a dot to the center of the shape."
        },
        {
            "category": "Figure Analysis (Paper Folding)",
            "question": "Fold square horizontal (Top to Bottom). Punch hole Bottom-Right. Unfold?",
            "options": ["Top-Right only", "Bottom-Right only", "Bottom-Right & Top-Right", "Four Corners"],
            "answer": "Bottom-Right & Top-Right",
            "explanation": "The horizontal fold mirrors the bottom-right hole to the top-right."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'Z'. Where is it hidden?",
            "options": ["Grid of squares", "Zig-zag line pattern", "Overlapping circles", "Triangle mesh"],
            "answer": "Zig-zag line pattern",
            "explanation": "A zig-zag pattern contains the sharp angles and lines to form a 'Z'."
        }
    ],
    "Paper 4": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Iron | Copper | Zinc",
            "options": ["Water", "Lead", "Wood", "Plastic", "Gas"],
            "answer": "Lead",
            "explanation": "Iron, Copper, and Zinc are metals. Lead is also a metal."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Doctor : Hospital :: Teacher : ______",
            "options": ["Study", "Book", "School", "Student", "Class"],
            "answer": "School",
            "explanation": "A Doctor works in a Hospital. A Teacher works in a School."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Happy | Joyful | Cheerful",
            "options": ["Sad", "Angry", "Glad", "Bored", "Tired"],
            "answer": "Glad",
            "explanation": "These are all synonyms for happiness. Glad is also a synonym."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[11 -> 13] and [15 -> 17]. Apply the same rule to [20 -> ?]",
            "options": ["21", "22", "23", "25", "24"],
            "answer": "22",
            "explanation": "Rule: Add 2. 20 + 2 = 22."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 100, 90, 80, 70, ___",
            "options": ["50", "65", "60", "55", "40"],
            "answer": "60",
            "explanation": "Subtract 10 pattern. 70 - 10 = 60."
        },
        {
            "category": "Number Analogies",
            "question": "[4 -> 16] and [3 -> 9]. Apply the same rule to [6 -> ?]",
            "options": ["12", "30", "36", "42", "24"],
            "answer": "36",
            "explanation": "Rule: Square the number. 6 * 6 = 36."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Dotted Circle. Shape 2: Dotted Square. Shape 3: Dotted Triangle. Which belongs?",
            "options": ["Solid Star", "Dotted Star", "Solid Hexagon", "Striped Circle"],
            "answer": "Dotted Star",
            "explanation": "The common feature is the dotted outline."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Vertical Line] -> [Horizontal Line]. Row 2: [Vertical Arrow] -> [?]",
            "options": ["Vertical Arrow", "Diagonal Arrow", "Horizontal Arrow", "Cross"],
            "answer": "Horizontal Arrow",
            "explanation": "Rule: Rotate 90 degrees."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Diagonally. Punch hole on the folded crease (Top Left). Unfold?",
            "options": ["One hole in center", "Two holes corners", "Four holes", "No holes"],
            "answer": "One hole in center",
            "explanation": "Punching exactly on the fold line results in a single hole (or joined holes) in the center when unfolded."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'T'. Where is it hidden?",
            "options": ["Curve pattern", "Hexagonal grid", "Square grid pattern", "Spiral"],
            "answer": "Square grid pattern",
            "explanation": "A square grid contains perpendicular lines that form a 'T'."
        }
    ],
    "Paper 5": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Oak | Elm | Pine",
            "options": ["Rose", "Ash", "Grass", "Leaf", "Bark"],
            "answer": "Ash",
            "explanation": "Oak, Elm, and Pine are types of trees. Ash is also a tree."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Puppy : Dog :: Kitten : ______",
            "options": ["Cat", "Mouse", "Pet", "Fur", "Animal"],
            "answer": "Cat",
            "explanation": "Puppy is the young of a Dog. Kitten is the young of a Cat."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Car | Bus | Truck",
            "options": ["Boat", "Plane", "Van", "Train", "Rocket"],
            "answer": "Van",
            "explanation": "These are all motor vehicles that travel on roads. Van is also a road vehicle."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[2 -> 5] and [3 -> 7]. Apply the same rule to [5 -> ?]",
            "options": ["10", "11", "9", "12", "15"],
            "answer": "11",
            "explanation": "Rule: (x2) + 1. 5 * 2 + 1 = 11."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 1, 2, 4, 7, 11, ___",
            "options": ["15", "16", "14", "18", "20"],
            "answer": "16",
            "explanation": "Pattern increases by +1, +2, +3, +4. Next is +5. 11 + 5 = 16."
        },
        {
            "category": "Number Analogies",
            "question": "[100 -> 10] and [81 -> 9]. Apply the same rule to [49 -> ?]",
            "options": ["7", "8", "6", "14", "24"],
            "answer": "7",
            "explanation": "Rule: Square Root. Sqrt(49) = 7."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Black Circle. Shape 2: Black Square. Shape 3: Black Triangle. Which belongs?",
            "options": ["White Circle", "Black Star", "Striped Square", "Grey Oval"],
            "answer": "Black Star",
            "explanation": "The common feature is that the shape is solid black (Shading)."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Square with X] -> [Square]. Row 2: [Circle with X] -> [?]",
            "options": ["Circle with X", "Circle", "Square", "Triangle"],
            "answer": "Circle",
            "explanation": "Rule: Remove the 'X' from inside the shape."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Top-to-Bottom. Then fold Left-to-Right. Punch Center. Unfold?",
            "options": ["1 hole", "2 holes", "4 holes", "8 holes"],
            "answer": "4 holes",
            "explanation": "Folding twice creates 4 layers. Punching once through 4 layers creates 4 holes."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'U'. Where is it hidden?",
            "options": ["Triangle grid", "Straight lines", "Chain link pattern", "Dot matrix"],
            "answer": "Chain link pattern",
            "explanation": "A chain link pattern contains curved loops that look like 'U'."
        }
    ],
    "Paper 6 (Harder)": [
        # Verbal (Nuanced & Scientific)
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Transparent | Translucent | Opaque",
            "options": ["See-through", "Solid", "Reflective", "Shiny", "Clear"],
            "answer": "Reflective",
            "explanation": "These are all properties of how materials interact with light (Optical properties). 'Reflective' fits this category better than 'Solid' (state of matter) or 'Clear' (which is a synonym for Transparent)."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Fragile : Break :: Elastic : ______",
            "options": ["Bend", "Stretch", "Rubber", "Snap", "Hard"],
            "answer": "Stretch",
            "explanation": "Fragile describes something prone to Breaking. Elastic describes something prone to Stretching."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Generous | Benevolent | Charitable",
            "options": ["Happy", "Rich", "Philanthropic", "Friendly", "Spending"],
            "answer": "Philanthropic",
            "explanation": "These words describe the act of giving to others. 'Philanthropic' is the closest formal synonym."
        },
        # Quantitative (Alternating & Complex)
        {
            "category": "Number Series",
            "question": "What comes next: 2, 10, 4, 20, 6, 30, ___",
            "options": ["8", "12", "40", "36", "60"],
            "answer": "8",
            "explanation": "This is an interleaved series. Series A: 2, 4, 6... (Next is 8). Series B: 10, 20, 30..."
        },
        {
            "category": "Number Analogies",
            "question": "[8 -> 3] and [12 -> 5]. Apply the same rule to [20 -> ?]",
            "options": ["9", "10", "8", "7", "11"],
            "answer": "9",
            "explanation": "Rule: Halve the number, then subtract 1. (8/2)-1=3. (20/2)-1=9."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 50, 45, 41, 38, 36, ___",
            "options": ["35", "34", "33", "30", "32"],
            "answer": "35",
            "explanation": "Subtract descending integers: -5, -4, -3, -2. Next is -1. 36 - 1 = 35."
        },
        # Non-Verbal (Conditional & Logic)
        {
            "category": "Figure Classification",
            "question": "Shape 1: 3-sided shape (Black). Shape 2: 4-sided shape (White). Shape 3: 5-sided shape (Black). Rule: Odd sides are Black, Even sides are White. Which belongs?",
            "options": ["6-sided (Black)", "6-sided (White)", "3-sided (White)", "4-sided (Black)"],
            "answer": "6-sided (White)",
            "explanation": "Logic: Even number of sides (6) must be White."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Circle] -> [Square]. Row 2: [Triangle] -> [?]. Rule: Add 1 side.",
            "options": ["Pentagon", "Square", "Hexagon", "Circle"],
            "answer": "Square",
            "explanation": "Circle (1 curve) -> Square (4) is not a clear add 1. Let's re-evaluate: Triangle (3) -> Square (4) is add 1 side."
        },
        {
            "category": "Figure Analysis",
            "question": "Square folded twice (Quarter size). Punch Hole through ALL layers in the Center. Unfold.",
            "options": ["1 Central Hole", "4 Central Holes", "4 Corner Holes", "2 Side Holes"],
            "answer": "4 Central Holes",
            "explanation": "Punching the center of a quarter-folded square means you punch near the 'folded corner' which is the center of the original paper. This creates 4 holes huddled in the center."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Number '4'. Where is it hidden?",
            "options": ["Circle patterns", "Triangle grid", "Overlapping squares", "A flag drawing"],
            "answer": "Triangle grid",
            "explanation": "The number 4 is composed of a triangle on a vertical stick. A grid of triangles contains this geometry."
        }
    ],
    "Paper 7 (Advanced)": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Rain | Hail | Snow",
            "options": ["Cloud", "Sleet", "Storm", "Water", "Cold"],
            "answer": "Sleet",
            "explanation": "These are all forms of precipitation. Sleet is another form."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Solar : Sun :: Lunar : ______",
            "options": ["Planet", "Star", "Moon", "Sky", "Space"],
            "answer": "Moon",
            "explanation": "Solar relates to the Sun. Lunar relates to the Moon."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Biology | Chemistry | Physics",
            "options": ["History", "Botany", "Literature", "Geography", "Art"],
            "answer": "Botany",
            "explanation": "These are natural sciences. Botany (study of plants) is a sub-branch of Biology/Science."
        },
        # Quantitative
        {
            "category": "Number Series",
            "question": "What comes next: 1, 1, 2, 3, 5, 8, ___",
            "options": ["10", "12", "13", "15", "11"],
            "answer": "13",
            "explanation": "Fibonacci Sequence: Add the previous two numbers. 5 + 8 = 13."
        },
        {
            "category": "Number Analogies",
            "question": "[4 -> 0.5] and [8 -> 1]. Apply the same rule to [20 -> ?]",
            "options": ["2", "2.5", "5", "10", "1.5"],
            "answer": "2.5",
            "explanation": "Rule: Divide by 8. 4/8=0.5, 8/8=1, 20/8=2.5."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 3, 6, 12, 24, ___",
            "options": ["36", "40", "48", "30", "50"],
            "answer": "48",
            "explanation": "Rule: Multiply by 2 (Doubling). 24 * 2 = 48."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Clock at 3:00. Shape 2: Clock at 9:00. Shape 3: Letter 'T'. Which belongs?",
            "options": ["Letter 'L'", "Letter 'V'", "Letter 'K'", "Clock at 2:00"],
            "answer": "Letter 'L'",
            "explanation": "The common feature is a 90-degree (Right) Angle."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Square] -> [Cube]. Row 2: [Triangle] -> [?]",
            "options": ["Pyramid", "Square", "Circle", "Cylinder"],
            "answer": "Pyramid",
            "explanation": "Rule: 2D shape becomes its 3D counterpart. Triangle becomes Pyramid (or Tetrahedron)."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Diagonally. Punch hole in the hypotenuse (long edge). Unfold.",
            "options": ["2 holes on edges", "2 holes in center", "1 hole", "4 holes"],
            "answer": "2 holes on edges",
            "explanation": "The hypotenuse of the folded triangle is the diagonal of the square. Punching it creates holes on the diagonal line."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'X'. Where is it hidden?",
            "options": ["Parallel lines", "Diamond Grid", "Circles", "Waves"],
            "answer": "Diamond Grid",
            "explanation": "A diamond grid is formed by intersecting diagonal lines, which create many 'X' shapes."
        }
    ],
    "Paper 8 (Complex Logic)": [
        # Verbal: Degree of Intensity & Function
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Cool : Cold :: Warm : ______",
            "options": ["Tepid", "Hot", "Boiling", "Freezing", "Heat"],
            "answer": "Hot",
            "explanation": "Degree of intensity. 'Cold' is a stronger version of 'Cool'. 'Hot' is the stronger version of 'Warm'."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Anxiety | Fear | Panic",
            "options": ["Bravery", "Terror", "Calm", "Sleep", "Emotion"],
            "answer": "Terror",
            "explanation": "These are all words describing increasing levels of fear/negative emotion. Terror fits this category."
        },
        # Quantitative: Ratios and Decimals
        {
            "category": "Number Series",
            "question": "What comes next: 0.2, 0.4, 0.8, 1.6, ___",
            "options": ["2.4", "3.0", "3.2", "1.8", "2.0"],
            "answer": "3.2",
            "explanation": "Doubling pattern with decimals. 1.6 * 2 = 3.2."
        },
        {
            "category": "Number Analogies",
            "question": "[4 -> 12] and [6 -> 18]. Apply the same rule to [15 -> ?]",
            "options": ["30", "45", "60", "20", "25"],
            "answer": "45",
            "explanation": "Rule: Multiply by 3. 15 * 3 = 45."
        },
        # Non-Verbal: Shape Addition & Intersections
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Left Half Circle] + [Right Half Circle] -> [Full Circle]. Row 2: [Top Half Square] + [?] -> [Full Square].",
            "options": ["Bottom Half Square", "Top Half Square", "Full Square", "Circle"],
            "answer": "Bottom Half Square",
            "explanation": "Addition Logic: Part A + Part B = Complete Shape."
        },
        {
            "category": "Figure Classification",
            "question": "Shape 1: Two intersecting Circles. Shape 2: Two intersecting Triangles. Shape 3: Two intersecting Squares. Which belongs?",
            "options": ["One Circle", "Two separated Circles", "Two intersecting Ovals", "Three Circles"],
            "answer": "Two intersecting Ovals",
            "explanation": "The rule is 'Two identical shapes intersecting'."
        },
        {
            "category": "Figure Analysis",
            "question": "Square folded in half (Rect). Folded again (Square). Punch hole in Top Right. Unfold.",
            "options": ["1 Hole Top Right", "4 Holes (Corners)", "2 Holes (Top)", "1 Hole Center"],
            "answer": "4 Holes (Corners)",
            "explanation": "Punching the open corner of a double-folded square affects all 4 outer corners of the original paper."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Chisel : Sculptor :: Scalpel : ______",
            "options": ["Artist", "Surgeon", "Doctor", "Hospital", "Nurse"],
            "answer": "Surgeon",
            "explanation": "Tool to Professional relationship. A chisel is the primary tool of a sculptor; a scalpel is the primary tool of a surgeon."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 1/2, 1/4, 1/8, 1/16, ___",
            "options": ["1/20", "1/24", "1/32", "1/18", "0"],
            "answer": "1/32",
            "explanation": "Halving the fraction each time (Denominator multiplies by 2)."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'A'. Where is it hidden?",
            "options": ["Pentagon Star", "Square Grid", "Circles", "Waves"],
            "answer": "Pentagon Star",
            "explanation": "The top point of a 5-pointed star contains the 'V' shape with a horizontal bar, forming an 'A'."
        }
    ],
    "Paper 9 (Spatial Mastery)": [
        # Verbal: Structural
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Inch | Foot | Yard",
            "options": ["Meter", "Mile", "Liter", "Gram", "Weight"],
            "answer": "Mile",
            "explanation": "These are all Imperial units of length. 'Meter' is Metric. 'Mile' is Imperial."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Leaf : Tree :: Petal : ______",
            "options": ["Stem", "Root", "Flower", "Garden", "Rose"],
            "answer": "Flower",
            "explanation": "Part to Whole relationship. A leaf is part of a tree; a petal is part of a flower."
        },
        # Quant: Time & Primes
        {
            "category": "Number Series",
            "question": "Time Sequence: 10:00, 10:15, 10:45, 11:30, ___",
            "options": ["12:00", "12:15", "12:30", "13:00", "11:45"],
            "answer": "12:30",
            "explanation": "Increasing intervals: +15 min, +30 min, +45 min. Next is +60 min (1 hour). 11:30 + 1hr = 12:30."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 2, 3, 5, 7, 11, ___",
            "options": ["12", "13", "14", "15", "17"],
            "answer": "13",
            "explanation": "Sequence of Prime Numbers."
        },
        # Non-Verbal: 3D & XOR
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Vertical Line] + [Horizontal Line] -> [Cross]. Row 2: [Diagonal /] + [Diagonal \] -> [?]",
            "options": ["X Shape", "Square", "Line", "Triangle"],
            "answer": "X Shape",
            "explanation": "Superposition: Combining two lines to form an intersection."
        },
        {
            "category": "Figure Classification",
            "question": "Shape 1: Cube. Shape 2: Cuboid. Shape 3: Cylinder. Which belongs?",
            "options": ["Square", "Circle", "Cone", "Triangle"],
            "answer": "Cone",
            "explanation": "3D Shapes (Solids). The options Square, Circle, Triangle are 2D."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Diagonally. Fold again to make small triangle. Punch center. Unfold.",
            "options": ["1 Hole", "2 Holes", "4 Holes", "8 Holes"],
            "answer": "4 Holes",
            "explanation": "Folding twice implies 4 layers. A single punch creates 4 symmetric holes."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Prologue | Introduction | Preface",
            "options": ["Chapter", "Ending", "Foreword", "Index", "Title"],
            "answer": "Foreword",
            "explanation": "These are all introductory sections of a book."
        },
        {
            "category": "Number Analogies",
            "question": "[7 -> 50] and [8 -> 57]. Apply the same rule to [6 -> ?]",
            "options": ["42", "43", "44", "45", "40"],
            "answer": "43",
            "explanation": "Rule: (x7) + 1. 6*7 = 42 + 1 = 43."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Letter 'M'. Where is it hidden?",
            "options": ["Two Mountain Peaks", "Ocean Waves", "Square Blocks", "Circles"],
            "answer": "Two Mountain Peaks",
            "explanation": "The silhouette of two pointed mountains creates the zigzag 'M' shape."
        }
    ],
    "Paper 10 (Challenge)": [
        # Verbal: Abstract
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Justice | Liberty | Freedom",
            "options": ["Law", "Court", "Equality", "Judge", "Police"],
            "answer": "Equality",
            "explanation": "Abstract societal values/ideals. Law/Court are institutions, not values."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Camera : Photography :: Microscope : ______",
            "options": ["Science", "Lab", "Biology", "Magnify", "Glass"],
            "answer": "Biology",
            "explanation": "Tool to Field of Study/Art. Cameras are used for Photography. Microscopes are used primarily for Biology."
        },
        # Quant: Complex
        {
            "category": "Number Series",
            "question": "What comes next: 4, 8, 6, 12, 10, 20, ___",
            "options": ["18", "22", "40", "16", "30"],
            "answer": "18",
            "explanation": "Alternating Operations: x2, -2, x2, -2... 10 * 2 = 20. 20 - 2 = 18."
        },
        {
            "category": "Number Analogies",
            "question": "[2 -> 9] and [3 -> 28]. Apply the same rule to [4 -> ?]",
            "options": ["64", "65", "17", "30", "50"],
            "answer": "65",
            "explanation": "Rule: Cubes + 1 (n^3 + 1). 4^3 = 64 + 1 = 65."
        },
        # Non-Verbal: Rotational & Perimeter
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Dot Top-Left] -> [Dot Top-Right]. Row 2: [Dot Bottom-Left] -> [?]. Rule: Move clockwise along corner.",
            "options": ["Dot Top-Left", "Dot Bottom-Right", "Dot Center", "No Dot"],
            "answer": "Dot Bottom-Right",
            "explanation": "Movement logic: The dot moves to the next corner clockwise."
        },
        {
            "category": "Figure Classification",
            "question": "Shape 1: 'S' shape. Shape 2: 'Z' shape. Shape 3: 'N' shape. Which belongs?",
            "options": ["Letter 'O'", "Letter 'H'", "Letter 'C'", "Letter 'D'"],
            "answer": "Letter 'H'",
            "explanation": "Rotational Symmetry. S, Z, and N look the same when rotated 180 degrees. H also shares this property."
        },
        {
            "category": "Figure Analysis",
            "question": "Square Folded Diagonally. Punch hole on the folded crease (center of diagonal). Unfold.",
            "options": ["2 Holes Center", "1 Hole Center", "4 Holes", "No Holes"],
            "answer": "1 Hole Center",
            "explanation": "Punching exactly on the fold line results in a single shape when unfolded (or two joined shapes appearing as one)."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Amble | Stroll | Saunter",
            "options": ["Run", "Sprint", "Walk", "Jump", "Hop"],
            "answer": "Walk",
            "explanation": "Synonyms for walking slowly/leisurely. 'Walk' is the general category verb that fits best among options (Run/Sprint are too fast)."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 3, 4, 7, 11, 18, 29, ___",
            "options": ["40", "47", "50", "35", "45"],
            "answer": "47",
            "explanation": "Fibonacci-style addition: 3+4=7, 4+7=11... 18+29=47."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Shape 'Diamond'. Where is it hidden?",
            "options": ["Square Grid", "Argyle Pattern (Sweater)", "Polka Dots", "Stripes"],
            "answer": "Argyle Pattern (Sweater)",
            "explanation": "An Argyle pattern consists entirely of repeating diamond shapes."
        }
    ]
}

# --- 2. SESSION STATE MANAGEMENT ---
# Initialize variables to track progress, score, and timer.

if 'current_paper' not in st.session_state:
    st.session_state.current_paper = None
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'finished' not in st.session_state:
    st.session_state.finished = False

# --- 3. HELPER FUNCTIONS ---

def start_quiz(paper_name):
    st.session_state.current_paper = paper_name
    st.session_state.quiz_active = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = []
    st.session_state.finished = False
    st.session_state.start_time = time.time()

def submit_answer(selected_option):
    paper = PAPERS[st.session_state.current_paper]
    current_q = paper[st.session_state.question_index]
    
    # Record answer
    is_correct = (selected_option == current_q['answer'])
    if is_correct:
        st.session_state.score += 1
    
    st.session_state.user_answers.append({
        "question": current_q['question'],
        "selected": selected_option,
        "correct": current_q['answer'],
        "explanation": current_q['explanation'],
        "is_correct": is_correct
    })
    
    # Move to next
    if st.session_state.question_index < len(paper) - 1:
        st.session_state.question_index += 1
    else:
        st.session_state.finished = True
        st.session_state.quiz_active = False

def restart():
    st.session_state.current_paper = None
    st.session_state.quiz_active = False
    st.session_state.finished = False

# --- 4. UI LAYOUT ---

st.set_page_config(page_title="CAT4 Practice App", page_icon="📝")

st.title("🧩 CAT4 Level D Practice (Grade 7)")

# A. HOME SCREEN
if not st.session_state.quiz_active and not st.session_state.finished:
    st.markdown("### Select a Practice Paper")
    st.info("You will have **10 minutes** to complete 10 questions.")
    
    # Grid Layout for 10 Papers
    # We will use 2 columns of 5 rows for a clean list look, or a grid.
    # Let's try a grid of 3 columns for standard, and 2 columns for advanced.
    
    st.markdown("#### Standard Papers")
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(1) # For Paper 7 to sit alone or with others if we reshuffle
    
    with row1[0]:
        if st.button("Start Paper 1", use_container_width=True):
            start_quiz("Paper 1")
            st.rerun()
    with row1[1]:
        if st.button("Start Paper 2", use_container_width=True):
            start_quiz("Paper 2")
            st.rerun()
    with row1[2]:
        if st.button("Start Paper 3", use_container_width=True):
            start_quiz("Paper 3")
            st.rerun()
            
    with row2[0]:
        if st.button("Start Paper 4", use_container_width=True):
            start_quiz("Paper 4")
            st.rerun()
    with row2[1]:
        if st.button("Start Paper 5", use_container_width=True):
            start_quiz("Paper 5")
            st.rerun()
    with row2[2]:
        if st.button("Start Paper 6 (Harder)", use_container_width=True):
            start_quiz("Paper 6 (Harder)")
            st.rerun()
            
    st.markdown("#### Advanced & Challenge Papers")
    row_adv_1 = st.columns(2)
    row_adv_2 = st.columns(2)

    with row_adv_1[0]:
        if st.button("Start Paper 7 (Advanced)", use_container_width=True):
            start_quiz("Paper 7 (Advanced)")
            st.rerun()
    with row_adv_1[1]:
        if st.button("Start Paper 8 (Complex Logic)", use_container_width=True):
            start_quiz("Paper 8 (Complex Logic)")
            st.rerun()
            
    with row_adv_2[0]:
        if st.button("Start Paper 9 (Spatial Mastery)", use_container_width=True):
            start_quiz("Paper 9 (Spatial Mastery)")
            st.rerun()
    with row_adv_2[1]:
        if st.button("Start Paper 10 (Challenge)", use_container_width=True):
            start_quiz("Paper 10 (Challenge)")
            st.rerun()

# B. QUIZ SCREEN
elif st.session_state.quiz_active:
    paper_data = PAPERS[st.session_state.current_paper]
    q_index = st.session_state.question_index
    question_data = paper_data[q_index]

    # Timer Logic
    elapsed_time = time.time() - st.session_state.start_time
    time_limit = 10 * 60 # 10 minutes in seconds
    remaining_time = time_limit - elapsed_time

    # Sidebar Status
    with st.sidebar:
        st.write(f"**Paper:** {st.session_state.current_paper}")
        st.write(f"**Question:** {q_index + 1} / {len(paper_data)}")
        
        # Timer Display
        if remaining_time > 0:
            mins, secs = divmod(int(remaining_time), 60)
            st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
        else:
            st.error("Time's Up!")
    
    # Check if time is up
    if remaining_time <= 0:
        st.warning("Time is up! Submitting your current progress...")
        time.sleep(2)
        st.session_state.finished = True
        st.session_state.quiz_active = False
        st.rerun()

    # Progress Bar
    st.progress((q_index) / len(paper_data))

    # Question Display
    st.subheader(f"Q{q_index + 1}: {question_data['category']}")
    st.write(f"**{question_data['question']}**")

    # Options
    # We use a distinct key for each question to reset selection
    selection = st.radio("Choose your answer:", question_data['options'], key=f"q_{q_index}", index=None)

    # Next Button
    if st.button("Submit Answer & Next" if q_index < 9 else "Finish Quiz", type="primary"):
        if selection:
            submit_answer(selection)
            st.rerun()
        else:
            st.warning("Please select an answer to proceed.")

# C. RESULTS SCREEN
elif st.session_state.finished:
    st.balloons()
    st.header("Quiz Complete!")
    
    final_score = st.session_state.score
    total_q = len(PAPERS[st.session_state.current_paper])
    percentage = int((final_score / total_q) * 100)
    
    # Score Card
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score", f"{final_score}/{total_q}")
    col2.metric("Percentage", f"{percentage}%")
    
    # Feedback Message
    if percentage >= 80:
        st.success("Excellent work! You are ready for the test.")
    elif percentage >= 50:
        st.warning("Good job. Review the explanations for the ones you missed.")
    else:
        st.error("Keep practicing. Focus on the Logic and Spatial sections.")

    st.divider()
    st.subheader("Detailed Review")

    for idx, ans in enumerate(st.session_state.user_answers):
        with st.expander(f"Q{idx+1}: {ans['question']} ({'✅ Correct' if ans['is_correct'] else '❌ Incorrect'})"):
            st.write(f"**Your Answer:** {ans['selected']}")
            st.write(f"**Correct Answer:** {ans['correct']}")
            st.info(f"**Explanation:** {ans['explanation']}")

    if st.button("Back to Home"):
        restart()
        st.rerun()