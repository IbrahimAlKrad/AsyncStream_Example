# AsyncStream with SwiftUI

StreamingEx is a simple SwiftUI demo showcasing the use of Swift's `AsyncStream` to simulate and visualize real-time data updates. The app generates random temperature values and updates the UI continuously until stopped.

---

## Overview

This project demonstrates the use of `AsyncStream` for creating and consuming asynchronous data streams in Swift.  
It focuses on:
- Generating simulated temperature readings asynchronously.
- Handling task cancellation safely.
- Updating SwiftUI views in real time on the main actor.

---

## Features

- Periodic data generation using Swift's concurrency model  
- Start/Stop controls for managing the stream  
- Automatic cleanup when the view disappears  
- Responsive SwiftUI interface with gradient background  

---

## How It Works

1. The `startStreaming()` method launches a task that runs an asynchronous stream of temperature values.  
2. The `AsyncStream<Int>` continuously emits a random value every 2 seconds until cancelled.  
3. Each emitted value is captured by a `for await` loop and used to update the `@State` property `currentValue`, which refreshes the SwiftUI view.  
4. The `stopStreaming()` method cancels the active task or is triggered automatically when the view disappears.

---

## Core Example

```
let stream = AsyncStream<Int> { continuation in
    Task.detached {
        while !Task.isCancelled {
            let temp = Int.random(in: 20...30)
            continuation.yield(temp)
            print("New value:", temp)
            try? await Task.sleep(nanoseconds: 2_000_000_000) // Wait 2 seconds
        }
            continuation.finish()
        }
    }
}
```

---

## User Interface

The app displays:
- A gradient background to enhance the visual appeal.
- A card showing the current temperature value.
- Buttons to start or stop live temperature streaming.

---

## Requirements

- iOS 17.0 or later  
- Xcode 15+  
- Swift 5.9 or later  

---

## Purpose

This example provides a practical demonstration of Swift concurrency using `AsyncStream`.  
It serves as a foundation for projects involving live data streams such as sensor input, telemetry, or other continuous feeds.
