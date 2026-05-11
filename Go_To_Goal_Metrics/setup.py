from setuptools import find_packages, setup

package_name = 'go_to_goal_metrics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ricardo Rosas',
    maintainer_email='ricardo.rosas@udlap.mx',
    description='ROS 2 package for turtle go-to-goal task with metrics collection.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_go_to_goal_metrics = go_to_goal_metrics.turtle_go_to_goal_metrics:main'
        ],
    },
)
