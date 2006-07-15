# Turn DeprecationWarnings off for fcntl
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='fcntl')

# Find and load updates
import updater
updater.loadupdates()

# Import iPodderGui (either directly or via the updates) and run it
iPodderGui = __import__('iPodderGui')
iPodderGui.main()
