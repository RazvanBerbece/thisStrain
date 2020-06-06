//
//  ViewController.swift
//  thisStrain
//
//  Created by Razvan-Antonio Berbece on 03/06/2020.
//  Copyright © 2020 Razvan-Antonio Berbece. All rights reserved.
//

import UIKit
import ARKit
import Foundation

class ViewController: UIViewController, ARSCNViewDelegate {
    
    @IBOutlet weak var analyserIndicator: UIActivityIndicatorView!
    
    /* AR Related Variables */
    @IBOutlet weak var sceneView: ARSCNView!
    var session : ARSession?
    let config = ARWorldTrackingConfiguration()
    
    /* WILL HOLD THE MOST RECENT STILL FRAME FROM THE SESSION */
    var imageFromARView : UIImage?
    
    /* Managers */
    let base64encoder = Base64Encoder()
    let client = Client()
    
    /* Labels holding scan results */
    @IBOutlet weak var strainResult: UILabel!
    @IBOutlet weak var accuracyResult: UILabel!
    
    /* Buttons and IBActions */
    @IBOutlet weak var captureButton: UIButton!
    
    @IBAction func sendImageForAnalysis() {
        
        self.analyserIndicator.startAnimating()
        
        self.captureSnapshotAndEnconde() {
            (base64Image) in
            self.client.sendPostWithData(base64string: base64Image) {
                (result) in
                self.strainResult.text = result[0]
                if let accuracy = Double(result[1]) {
                    self.accuracyResult.text = String(format: "%.2f", accuracy) + "% accurate"
                    self.analyserIndicator.stopAnimating()
                }
            }
        }
        
    }
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        
        /* Config AR session */
        self.sceneView.delegate = self
        self.session = self.sceneView.session
        self.session!.run(config)
        
    }
    
    /* Helper functions */
    func captureSnapshotAndEnconde(completion: @escaping (String) -> Void) {
        
        /* Get current view as UIImage */
        self.imageFromARView = self.sceneView.snapshot()
        
        let base64stringImage = self.base64encoder.imageToBase64(image: self.imageFromARView!)
        
        completion(base64stringImage)
        
    }
    
    
}

