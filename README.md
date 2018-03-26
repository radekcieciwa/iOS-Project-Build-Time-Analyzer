# iOS-Project-Build-Time-Analyzer
More detailed build time measuring tool for iOS projects.


## Example usage
### Enable detailed build logs

By default they don't exist
```
defaults write com.apple.dt.xcodebuild CommandLineBuildTimingLogLevel -int 5
```

So after executing it, you should remove the flag in order to remove any custom logs.
```
defaults delete com.apple.dt.xcodebuild CommandLineBuildTimingLogLevel
```

### Generate build.log
```
script -q /dev/null xcodebuild clean build -workspace brainly.xcworkspace -scheme Brainly -destination "platform=iOS Simulator,name=iPhone 5s" | grep CommandLineBuildTiming | cut -d " " -f 6- | grep -v REAL | sed -e 's/|//' > build.log
```

### Use python script to parse output build output
```
python parse_build_log.py ./Example/build.log
```
