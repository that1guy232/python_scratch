import unittest

import TestCPU_ADC
import TestCPU_BRK
import TestCPU_LDA
import TestCPU_LDX
import TestCPU_LDY
import TestCPU_STA
import TestCPU_TXI
import TestCPU_AND
import TestCPU_SBC

# Create a test suite combining all the test cases
suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_ADC))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_BRK))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_LDA))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_LDX))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_LDY))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_STA))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_TXI))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_AND))
suite.addTests(unittest.TestLoader().loadTestsFromModule(TestCPU_SBC))
# Run the combined test suite
unittest.TextTestRunner().run(suite)

