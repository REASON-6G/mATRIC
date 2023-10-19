// app.component.ts

import { Component, OnInit } from '@angular/core';
import { AccessTechService } from './access-technology.service';  // Update this path

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  accessTechnologies: any[] = [];

  constructor(private atService: AccessTechService) {}  // Using the correct class name here

  ngOnInit(): void {
    this.atService.getAccessTechnologies().subscribe((data) => {
      this.accessTechnologies = data;
    });
  }
}
