//
//  ContentView.swift
//  StreamingEx
//
//  Created by Ibrahim Al Krad on 10.11.25.
//
//  This SwiftUI view simulates a streaming temperature sensor UI.
//  It periodically updates a displayed temperature value using AsyncStream.
//

import SwiftUI

struct ContentView: View {
    // Latest temperature value (nil means no data yet)
    @State private var currentValue: Int? = nil
    
    // Streaming control flag
    @State private var isStreaming = false
    
    // Active streaming task reference for cancellation
    @State private var streamTask: Task<Void, Never>? = nil

    var body: some View {
        ZStack {
            // Background gradient for visual depth
            LinearGradient(
                colors: [.blue.opacity(0.2), .teal.opacity(0.4)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 30) {
                // App title
                Text("Home Sensor")
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundStyle(.white)
                    .shadow(radius: 3)

                // Sensor display card
                ZStack {
                    RoundedRectangle(cornerRadius: 25)
                        .fill(.white)
                        .shadow(radius: 10)

                    VStack(spacing: 16) {
                        Text("Temperature")
                            .font(.headline)
                            .foregroundColor(.gray)

                        // Show current temperature or placeholder
                        Text(currentValue.map { "\($0)°C" } ?? "--")
                            .font(.system(size: 64, weight: .bold, design: .rounded))
                            .foregroundStyle(.orange)
                    }
                    .padding(40)
                }
                .frame(width: 250, height: 220)

                // Start/Stop streaming controls
                HStack(spacing: 40) {
                    Button(action: startStreaming) {
                        Label("Start", systemImage: "play.circle.fill")
                            .font(.title2)
                    }
                    .disabled(isStreaming) // Disable if already streaming

                    Button(action: stopStreaming) {
                        Label("Stop", systemImage: "stop.circle.fill")
                            .font(.title2)
                    }
                    .disabled(!isStreaming) // Disable if not streaming
                }
                .foregroundStyle(.white)
            }
            .padding()
        }
        .onDisappear {
            // Automatically stop streaming when leaving the view
            stopStreaming()
        }
    }

    // MARK: - Streaming logic

    /// Starts the simulated temperature stream.
    func startStreaming() {
        // Cancel any existing task before starting a new one
        streamTask?.cancel()

        isStreaming = true
        streamTask = Task {
            await runAsyncStream()
        }
    }

    /// Stops the current temperature stream.
    func stopStreaming() {
        streamTask?.cancel()
        streamTask = nil
        isStreaming = false
    }

    /// Handles the logic of generating and consuming a simulated async stream.
    func runAsyncStream() async {
        // Create an async stream producing random temperatures every 2 seconds
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

        // Consume the stream and update UI
        for await item in stream {
            guard !Task.isCancelled else { break }
            await MainActor.run {
                currentValue = item
            }
        }
    }
}

#Preview {
    ContentView()
}
